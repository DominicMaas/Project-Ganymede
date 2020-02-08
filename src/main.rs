extern crate blurz;
extern crate gphoto;

use std::{thread, time};

/// A function which loops forever until a camera is found
fn detect_camera() -> gphoto::Camera {
    // Get the context
    let mut context = gphoto::Context::new().unwrap();

    // Run in a loop until we have a camera
    loop {
        // Attempt to get the camera
        let camera = gphoto::Camera::autodetect(&mut context);

        // If there was an error, wait 10 seconds and try again
        if camera.is_err() {
            println!("Camera not connected to device, trying again in 10 seconds...");
            thread::sleep(time::Duration::from_secs(10));
        } else {
            // Return the camera
            println!("Camera connected!");
            return camera.unwrap();
        }
    }
}

fn main() {
    println!("Starting Program...");

    // Attempt to get the camera
    let camera = detect_camera();
    let abilities = camera.abilities();

    println!("\n[abilities]");
    println!("      device type = {:?}", abilities.device_type());
    println!("            model = {:?}", abilities.model());
    println!("    driver status = {:?}", abilities.driver_status());
    println!("       port types = {:?}", abilities.port_types());
    println!("           speeds = {:?}", abilities.speeds());
    println!("camera operations = {:?}", abilities.camera_operations());
    println!("  file operations = {:?}", abilities.file_operations());
    println!("folder operations = {:?}", abilities.folder_operations());
    println!("       USB vendor = {:?}", abilities.usb_vendor());
    println!("      USB product = {:?}", abilities.usb_product());
    println!("        USB class = {:?}", abilities.usb_class());
    println!("     USB subclass = {:?}", abilities.usb_subclass());
    println!("     USB protocol = {:?}", abilities.usb_protocol());

    // Create a session
    // let session = Session::create_session(Option::None).unwrap();
    // let adapter = Adapter::init(&session).unwrap();

    // Temp
    // let device = adapter.get_first_device().unwrap();
    // println!("{:?}", device);
}
