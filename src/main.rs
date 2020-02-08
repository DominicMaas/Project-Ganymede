extern crate blurz;
extern crate gphoto;

use std::process::Command;
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

/// Main entry
fn main() {
    println!("Starting Program...");

    // Attempt to get the camera
    detect_camera();

    // We don't need to use the camera, just use the
    // library to ensure a camera is connected, use the commands
    // for the rest. TODO: Also use library, library does not support
    // commands.

    set_iso(3);

    let iso = get_iso();
    println!("current iso: {}", iso.current);

    // Create a session
    // let session = Session::create_session(Option::None).unwrap();
    // let adapter = Adapter::init(&session).unwrap();

    // Temp
    // let device = adapter.get_first_device().unwrap();
    // println!("{:?}", device);
}

struct ISO {
    current: String,
}

fn set_iso(number: i16) {
    let cmd = Command::new("gphoto2")
        .arg("--set-config")
        .arg(format!("iso={}", number))
        .output()
        .expect("Command did not run");

    println!("status: {}", cmd.status);
    println!("stdout: {}", String::from_utf8_lossy(&cmd.stdout));
    println!("stderr: {}", String::from_utf8_lossy(&cmd.stderr));
}

// TODO

fn get_iso() -> ISO {
    let cmd = Command::new("gphoto2")
        .arg("--get-config")
        .arg("iso")
        .output()
        .expect("Command did not run");
    let result = String::from_utf8_lossy(&cmd.stdout);

    println!("status: {}", cmd.status);
    println!("stdout: {}", String::from_utf8_lossy(&cmd.stdout));
    println!("stderr: {}", String::from_utf8_lossy(&cmd.stderr));

    return ISO {
        current: String::from(result),
    };
}
