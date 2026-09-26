#!/usr/bin/env python3
"""
TAP-001 HSIE Builder
Python 3.6.9 compatible.
Standard library only.

Provides:
  - Tkinter GUI
  - CLI JSON input/output
  - HSIE structure validation
  - No cryptographic material generation
"""

from __future__ import print_function

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone

try:
    import tkinter as tk
    from tkinter import messagebox, filedialog
except ImportError:
    print("Tkinter is not available in this Python installation.", file=sys.stderr)
    print("Install the OS package that provides Tkinter, then run this program again.",
          file=sys.stderr)
    raise


SCHEMA_VERSION = "1.2"

FIELD_DEFINITIONS = [
    ("record_type", "Record Type"),
    ("record_id", "Record ID"),
    ("record_version", "Record Version"),
    ("schema_version", "Schema Version"),

    ("key_identifier", "Key Identifier"),
    ("public_key", "Public Verification Key"),
    ("signature_algorithm", "Signature Algorithm"),
    ("signature_parameters", "Signature Parameters"),

    ("start_time", "Start Time (UTC)"),
    ("end_time", "End Time (UTC)"),

    ("latitude", "Latitude"),
    ("longitude", "Longitude"),
    ("coordinate_reference_system", "Coordinate Reference System"),
    ("coordinate_precision", "Coordinate Precision"),

    ("physical_medium", "Physical Medium"),
    ("custody_access", "Custody / Access"),
    ("destruction", "Destruction"),
    ("supporting_records", "Supporting Records"),
    ("integrity_metadata", "Integrity Metadata"),

    ("message_id", "Message ID (optional)"),
    ("message_creation_time", "Message Creation Time (optional)"),
    ("message_role", "Message Role (optional)"),
    ("message_content", "Message Content (optional)"),
    ("channel", "Channel (optional)"),
    ("cryptographic_protection", "Cryptographic Protection (optional)"),

    ("commitment_version", "Commitment Version (optional)"),
    ("hash_algorithm", "Hash Algorithm (optional)"),
    ("hash_parameters", "Hash Parameters (optional)"),
    ("domain_separator", "Domain Separator (optional)"),
    ("secret_key_encoding", "Secret Key Encoding (optional)"),
    ("commitment_value", "Commitment Value (optional)"),
    ("commitment_public_key_identifier", "Commitment Public Key Identifier (optional)"),
]


EXAMPLE_VALUES = {
    "record_type": "HSIE_RECORD",
    "record_id": "550e8400-e29b-41d4-a716-446655440000",
    "record_version": "1",
    "schema_version": SCHEMA_VERSION,

    "key_identifier": "historical-signing-key-001",
    "public_key": "EXAMPLE_PUBLIC_VERIFICATION_KEY",
    "signature_algorithm": "EXAMPLE_SIGNATURE_ALGORITHM",
    "signature_parameters": '{"example": "parameters"}',

    "start_time": "2026-09-25T00:00:00Z",
    "end_time": "2026-09-25T00:05:00Z",

    "latitude": "0.000000",
    "longitude": "0.000000",
    "coordinate_reference_system": "WGS84",
    "coordinate_precision": "1 meter",

    "physical_medium": '{"type": "example-medium", "identifier": "MEDIUM-001"}',
    "custody_access": '{"custodian": "example", "access_conditions": "example"}',
    "destruction": '{"method": "example", "performed": true}',
    "supporting_records": '[]',
    "integrity_metadata": '{"hash_algorithm": "SHA-256", "integrity_value": "EXAMPLE_INTEGRITY_VALUE"}',

    "message_id": "MSG-001",
    "message_creation_time": "2026-09-25T00:06:00Z",
    "message_role": "outgoing_request",
    "message_content": "BASE64URL_CIPHERTEXT",
    "channel": "temporal-message-channel",
    "cryptographic_protection": '{"scheme": "example"}',

    "commitment_version": "1",
    "hash_algorithm": "SHA-256",
    "hash_parameters": '{"output_length": 256}',
    "domain_separator": "TAP-001-HSIE",
    "secret_key_encoding": "base64url",
    "commitment_value": "EXAMPLE_COMMITMENT_VALUE",
    "commitment_public_key_identifier": "example-commitment-key-001",
}


REQUIRED_FIELDS = [
    "record_type",
    "record_id",
    "record_version",
    "schema_version",
    "key_identifier",
    "public_key",
    "signature_algorithm",
    "signature_parameters",
    "start_time",
    "end_time",
    "latitude",
    "longitude",
    "coordinate_reference_system",
    "coordinate_precision",
    "physical_medium",
    "custody_access",
    "destruction",
    "supporting_records",
    "integrity_metadata",
]


def validate_uuid4(value, field_name):
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError):
        raise ValueError("%s must contain a valid UUID." % field_name)

    if parsed.version != 4:
        raise ValueError("%s must contain a UUIDv4." % field_name)


def validate_timestamp(value, field_name):
    if not isinstance(value, str):
        raise ValueError("%s must be a string." % field_name)

    if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", value):
        raise ValueError(
            "%s must use RFC3339 UTC form YYYY-MM-DDTHH:MM:SSZ." % field_name
        )

    try:
        # Python 3.6-compatible replacement for datetime.fromisoformat().
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError as exc:
        raise ValueError("%s must contain a valid timestamp." % field_name) from exc


def parse_json_object_or_array(value, field_name):
    try:
        parsed = json.loads(value)
    except (ValueError, TypeError) as exc:
        raise ValueError("%s must contain valid JSON." % field_name) from exc

    if not isinstance(parsed, (dict, list)):
        raise ValueError("%s must contain a JSON object or array." % field_name)

    return parsed


def require_nonempty(data, field_name):
    value = data.get(field_name)
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError("%s is required." % field_name)
    return value


def build_hsie(data):
    """
    Validate input fields and return the complete HSIE as a Python dict.

    This function does not generate cryptographic keys, signatures, hashes,
    ciphertext, or other cryptographic values. Those values must be supplied.
    """
    if not isinstance(data, dict):
        raise ValueError("HSIE input must be a JSON object.")

    for field_name in REQUIRED_FIELDS:
        require_nonempty(data, field_name)

    if data["record_type"] != "HSIE_RECORD":
        raise ValueError("record_type must be HSIE_RECORD.")

    validate_uuid4(data["record_id"], "record_id")

    try:
        record_version = int(data["record_version"])
    except (ValueError, TypeError):
        raise ValueError("record_version must be a positive integer.")

    if record_version <= 0:
        raise ValueError("record_version must be a positive integer.")

    if data["schema_version"] != SCHEMA_VERSION:
        raise ValueError(
            "schema_version must be %s." % SCHEMA_VERSION
        )

    start_time = validate_timestamp(data["start_time"], "start_time")
    end_time = validate_timestamp(data["end_time"], "end_time")

    if end_time < start_time:
        raise ValueError("end_time must not be earlier than start_time.")

    try:
        latitude = float(data["latitude"])
    except (ValueError, TypeError):
        raise ValueError("latitude must be numeric.")

    try:
        longitude = float(data["longitude"])
    except (ValueError, TypeError):
        raise ValueError("longitude must be numeric.")

    if latitude < -90.0 or latitude > 90.0:
        raise ValueError("latitude must be between -90 and 90.")

    if longitude < -180.0 or longitude > 180.0:
        raise ValueError("longitude must be between -180 and 180.")

    json_fields = [
        ("signature_parameters", data["signature_parameters"]),
        ("physical_medium", data["physical_medium"]),
        ("custody_access", data["custody_access"]),
        ("destruction", data["destruction"]),
        ("supporting_records", data["supporting_records"]),
        ("integrity_metadata", data["integrity_metadata"]),
    ]

    parsed = {}
    for field_name, value in json_fields:
        parsed[field_name] = parse_json_object_or_array(value, field_name)

    message = None
    if str(data.get("message_id", "")).strip():
        require_nonempty(data, "message_creation_time")
        require_nonempty(data, "message_role")
        require_nonempty(data, "message_content")
        require_nonempty(data, "channel")
        require_nonempty(data, "cryptographic_protection")

        validate_timestamp(
            data["message_creation_time"],
            "message_creation_time"
        )

        message = {
            "message_id": data["message_id"],
            "creation_time": data["message_creation_time"],
            "message_role": data["message_role"],
            "content": data["message_content"],
            "channel": data["channel"],
            "cryptographic_protection": parse_json_object_or_array(
                data["cryptographic_protection"],
                "cryptographic_protection"
            ),
        }

    commitment = None
    if str(data.get("commitment_version", "")).strip():
        commitment_required = [
            "hash_algorithm",
            "hash_parameters",
            "domain_separator",
            "secret_key_encoding",
            "commitment_value",
            "commitment_public_key_identifier",
        ]

        for field_name in commitment_required:
            require_nonempty(data, field_name)

        try:
            commitment_version = int(data["commitment_version"])
        except (ValueError, TypeError):
            raise ValueError("commitment_version must be an integer.")

        if commitment_version <= 0:
            raise ValueError("commitment_version must be positive.")

        commitment = {
            "commitment_version": commitment_version,
            "hash_algorithm": data["hash_algorithm"],
            "hash_parameters": parse_json_object_or_array(
                data["hash_parameters"],
                "hash_parameters"
            ),
            "domain_separator": data["domain_separator"],
            "secret_key_encoding": data["secret_key_encoding"],
            "commitment_value": data["commitment_value"],
            "commitment_public_key_identifier":
                data["commitment_public_key_identifier"],
        }

    result = {
        "record_type": data["record_type"],
        "record_id": data["record_id"],
        "record_version": record_version,
        "schema_version": data["schema_version"],

        "authentication_material": {
            "key_identifier": data["key_identifier"],
            "public_key": data["public_key"],
            "signature_algorithm": data["signature_algorithm"],
            "signature_parameters": parsed["signature_parameters"],
        },

        "temporal_interval": {
            "start_time": data["start_time"],
            "end_time": data["end_time"],
        },

        "location": {
            "latitude": latitude,
            "longitude": longitude,
            "coordinate_reference_system":
                data["coordinate_reference_system"],
            "coordinate_precision": data["coordinate_precision"],
        },

        "physical_event": {
            "physical_medium": parsed["physical_medium"],
            "custody_access": parsed["custody_access"],
            "destruction": parsed["destruction"],
            "supporting_records": parsed["supporting_records"],
            "integrity_metadata": parsed["integrity_metadata"],
        },
    }

    if message is not None:
        result["associated_outgoing_message"] = message

    if commitment is not None:
        result["optional_secret_commitment"] = commitment

    return result


def load_input_file(filename):
    with open(filename, "r") as handle:
        data = json.load(handle)

    return data


def save_json(data, filename):
    with open(filename, "w") as handle:
        json.dump(data, handle, indent=2, sort_keys=False)
        handle.write("\n")


def run_cli(args):
    try:
        input_data = load_input_file(args.input)
        hsie = build_hsie(input_data)
    except Exception as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        return 1

    output = json.dumps(hsie, indent=2, sort_keys=False)

    if args.output:
        try:
            save_json(hsie, args.output)
        except Exception as exc:
            print("ERROR writing output: %s" % exc, file=sys.stderr)
            return 1
        print("HSIE written to %s" % args.output)
    else:
        print(output)

    return 0


class HsieBuilderApp(object):
    def __init__(self, root):
        self.root = root
        self.root.title("TAP-001 HSIE Builder")
        self.root.geometry("900x900")

        self.entries = {}

        self.build_ui()
        self.populate_examples()

    def add_field(self, parent, row, name, label):
        tk.Label(
            parent,
            text=label,
            anchor="w"
        ).grid(row=row, column=0, sticky="w", padx=5, pady=3)

        entry = tk.Entry(parent, width=85)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=3)

        self.entries[name] = entry

    def add_section(self, parent, title, fields):
        frame = tk.LabelFrame(parent, text=title, padx=5, pady=5)
        frame.pack(fill="x", padx=8, pady=5)
        frame.columnconfigure(1, weight=1)

        for row, name in enumerate(fields):
            label = dict(FIELD_DEFINITIONS)[name]
            self.add_field(frame, row, name, label)

    def build_ui(self):
        # Scrollable main form so the complete HSIE editor can be reached
        # on smaller screens.
        form_container = tk.Frame(self.root)
        form_container.pack(fill="both", expand=True)

        form_canvas = tk.Canvas(form_container, highlightthickness=0)
        form_scrollbar = tk.Scrollbar(
            form_container,
            orient="vertical",
            command=form_canvas.yview
        )
        form_canvas.configure(yscrollcommand=form_scrollbar.set)

        form_scrollbar.pack(side="right", fill="y")
        form_canvas.pack(side="left", fill="both", expand=True)

        top = tk.Frame(form_canvas)
        form_window = form_canvas.create_window(
            (0, 0),
            window=top,
            anchor="nw"
        )

        def update_scroll_region(event):
            form_canvas.configure(scrollregion=form_canvas.bbox("all"))

        def resize_form(event):
            form_canvas.itemconfigure(form_window, width=event.width)

        top.bind("<Configure>", update_scroll_region)
        form_canvas.bind("<Configure>", resize_form)

        self.add_section(
            top,
            "Record Metadata",
            [
                "record_type",
                "record_id",
                "record_version",
                "schema_version",
            ],
        )

        self.add_section(
            top,
            "Authentication Material",
            [
                "key_identifier",
                "public_key",
                "signature_algorithm",
                "signature_parameters",
            ],
        )

        self.add_section(
            top,
            "Temporal Interval",
            [
                "start_time",
                "end_time",
            ],
        )

        self.add_section(
            top,
            "Location",
            [
                "latitude",
                "longitude",
                "coordinate_reference_system",
                "coordinate_precision",
            ],
        )

        self.add_section(
            top,
            "Physical Event",
            [
                "physical_medium",
                "custody_access",
                "destruction",
                "supporting_records",
                "integrity_metadata",
            ],
        )

        self.add_section(
            top,
            "Associated Outgoing Message (optional)",
            [
                "message_id",
                "message_creation_time",
                "message_role",
                "message_content",
                "channel",
                "cryptographic_protection",
            ],
        )

        self.add_section(
            top,
            "Optional Secret Commitment",
            [
                "commitment_version",
                "hash_algorithm",
                "hash_parameters",
                "domain_separator",
                "secret_key_encoding",
                "commitment_value",
                "commitment_public_key_identifier",
            ],
        )

        # Fixed controls/output area below the scrollable form.
        bottom = tk.Frame(self.root)
        bottom.pack(fill="both", expand=False)

        button_frame = tk.Frame(bottom)
        button_frame.pack(fill="x", padx=8, pady=8)

        tk.Button(
            button_frame,
            text="Build HSIE",
            command=self.build
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Save JSON",
            command=self.save
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Clear Output",
            command=self.clear_output
        ).pack(side="left", padx=5)

        output_frame = tk.LabelFrame(
            bottom,
            text="Built HSIE JSON",
            padx=5,
            pady=5
        )
        output_frame.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=5
        )

        self.output = tk.Text(
            output_frame,
            wrap="none",
            height=20
        )
        self.output.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            output_frame,
            command=self.output.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.output.configure(yscrollcommand=scrollbar.set)

    def populate_examples(self):
        for name, value in EXAMPLE_VALUES.items():
            entry = self.entries.get(name)
            if entry is not None:
                entry.delete(0, tk.END)
                entry.insert(0, value)

    def collect_data(self):
        data = {}
        for name, entry in self.entries.items():
            data[name] = entry.get()
        return data

    def build(self):
        try:
            hsie = build_hsie(self.collect_data())
        except Exception as exc:
            messagebox.showerror("HSIE Validation Error", str(exc))
            return

        self.output.delete("1.0", tk.END)
        self.output.insert(
            tk.END,
            json.dumps(hsie, indent=2, sort_keys=False)
        )

    def save(self):
        try:
            hsie = build_hsie(self.collect_data())
        except Exception as exc:
            messagebox.showerror("HSIE Validation Error", str(exc))
            return

        filename = filedialog.asksaveasfilename(
            title="Save HSIE JSON",
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("All files", "*.*"),
            ],
        )

        if not filename:
            return

        try:
            save_json(hsie, filename)
        except Exception as exc:
            messagebox.showerror(
                "Save Error",
                "Unable to save HSIE:\n%s" % exc
            )
            return

        messagebox.showinfo(
            "HSIE Saved",
            "HSIE JSON saved to:\n%s" % filename
        )

    def clear_output(self):
        self.output.delete("1.0", tk.END)


def main():
    parser = argparse.ArgumentParser(
        description="Build and validate a TAP-001 HSIE."
    )
    parser.add_argument(
        "--input",
        help="JSON input file containing HSIE field values."
    )
    parser.add_argument(
        "--output",
        help="Write the built HSIE JSON to this file."
    )

    args = parser.parse_args()

    if args.input:
        return run_cli(args)

    root = tk.Tk()
    HsieBuilderApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
