#! Speed of light in vacuum - Physical Constant
## Symbol: c
## The speed of light in vacuum is a constant value exactly equal to 
#! 299,792,458 meters per second.

#! Meter - Unit of Length
## Symbol: m
## The meter is the length of the path traveled by light in a vacuum in
#! 1/299,792,458 of a second.

#! Second - Unit of Time
## Symbol: s
## The second is defined by taking the fixed numerical value of the 
## cesium frequency, the unperturbed groud-state hyperfine transition 
## frequency of the cesium-133 atom, to be 9,192,631,770 when expressed 
#! in the unit Hz.

#! Light Year - Distance Measurement
## Symbol: ly
## A light-year is the distance a beam of light travels in a single 
## Earth year, which is 9.46073 x 10 to the 12th power km
#! (6 trillion miles).

#! Epoch Time - Unit of Time Measurement
## Symbol: et
## The total number of non-leap seconds having elapsed since the 
#! Unix epoch on 00:00:00 UTC January 1, 1970.

#! Galactic Center of Milky Way - Location
## Symbol: gc_milky_way
## The Galactic Center of the Milky Way galaxy is a supermassive 
## black hole of about 4 million solar masses called Sagitarious A,
## approximately 8 kiloparsecs (26000 ly) away from Earth
#! at Galactic Coordinates 17h 45m 40.0409s,-29 degrees 00' 28.118.

->lib:io:default:Observer
->lib:io:default:Time
->lib:io:default:Location
->lib:io:USF

framework:USF;

self:Observer;
self.et = Time.now.et;
self.reference_entity(gc_milky_way);
self.x = Location.4d.x(Location.here.galactic_coordinates);
self.y = Location.4d.y(Location.here.galactic_coordinates);
self.z = Location.4d.z(Location.here.galactic_coordinates);

def move_observer(
	observer,
	target_et,
	target_x,
	target_y,
	target_z
) {
	:
		observer.et.verify();
		observer.reference_entity.verify();
		observer.x.verify();
		observer.y.verify();
		observer.z.verify();
		observer.set_restore_point();
		observer.et = target_et;
		observer.x(observer.reference_entity) = target_x;
		observer.y(observer.reference_entity) = target_y;
		observer.z(observer.reference_entity) = target_z;
		observer.commit();
		observer.et.verify();
		observer.x.verify();
		observer.y.verify();
		observer.z.verify();
		framework.Log("Observer moved successfully.");		
		ret 0;
	~->err
		framework.HandleError(0, "move_observer", ("Failed to move Observer: " + err.msg));
		observer.restore();
		ret 1;
}

def main() {

	move_observer(self, (self.et - 300), self.x, self.y, self.z);
	move_observer(self, (self.et + 300), self.x, self.y, self.z);
	move_observer(self, (self.et + 300), self.x, self.y, self.z);
	move_observer(self, (self.et - 300), self.x, self.y, self.z);
}
