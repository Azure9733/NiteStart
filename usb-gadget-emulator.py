import os
import subprocess
import time

class USBGadgetEmulator:
    def __init__(self, gadget_name='nitestart', file_path='/tmp/virtual_disk.img'):
        self.gadget_name = gadget_name
        self.file_path = file_path
        self.gadget_path = f'/sys/kernel/config/usb_gadget/{gadget_name}'

    def create_disk_image(self, size_mb=100):
        """Create a virtual disk image"""
        try:
            subprocess.run([
                'dd', 'if=/dev/zero', f'of={self.file_path}', 
                'bs=1M', f'count={size_mb}'
            ], check=True)
            subprocess.run(['mkfs.vfat', self.file_path], check=True)
            print(f"Created {size_mb}MB virtual disk image")
        except subprocess.CalledProcessError as e:
            print(f"Error creating disk image: {e}")
            return False
        return True

    def setup_gadget(self):
        """Set up USB Gadget configuration"""
        try:
            # Create gadget directory
            os.makedirs(self.gadget_path, exist_ok=True)
            
            # Set vendor and product IDs
            with open(f'{self.gadget_path}/idVendor', 'w') as f:
                f.write('0x1d6b')  # Linux Foundation
            with open(f'{self.gadget_path}/idProduct', 'w') as f:
                f.write('0x0104')  # Mass Storage
            
            # Create English language strings
            os.makedirs(f'{self.gadget_path}/strings/0x409', exist_ok=True)
            with open(f'{self.gadget_path}/strings/0x409/manufacturer', 'w') as f:
                f.write('NiteStart')
            with open(f'{self.gadget_path}/strings/0x409/product', 'w') as f:
                f.write('Virtual USB Drive')
            
            # Create configuration
            os.makedirs(f'{self.gadget_path}/configs/c.1/strings/0x409', exist_ok=True)
            with open(f'{self.gadget_path}/configs/c.1/strings/0x409/configuration', 'w') as f:
                f.write('Mass Storage')
            
            # Create mass storage function
            os.makedirs(f'{self.gadget_path}/functions/mass_storage.usb0', exist_ok=True)
            with open(f'{self.gadget_path}/functions/mass_storage.usb0/lun.0/file', 'w') as f:
                f.write(self.file_path)
            
            # Link function to configuration
            os.symlink(
                f'{self.gadget_path}/functions/mass_storage.usb0', 
                f'{self.gadget_path}/configs/c.1/mass_storage.usb0'
            )
            
            # Activate the gadget
            with open('/sys/kernel/config/usb_gadget/nitestart/UDC', 'w') as f:
                f.write(self._get_udc_device())
            
            print("USB Gadget configured successfully")
            return True
        except Exception as e:
            print(f"Error setting up USB Gadget: {e}")
            return False

    def _get_udc_device(self):
        """Get the UDC (USB Device Controller) device"""
        try:
            with open('/sys/class/udc/dummy_udc/device/uevent', 'r') as f:
                return f.read().strip().split('=')[-1]
        except:
            print("Could not find UDC device. Requires specific USB controller support.")
            return ''

    def cleanup(self):
        """Clean up USB Gadget configuration"""
        try:
            # Disable the gadget
            with open(f'{self.gadget_path}/UDC', 'w') as f:
                f.write('\n')
            
            # Remove symlinks and directories
            subprocess.run(['rm', '-rf', self.gadget_path], check=True)
            print("USB Gadget cleaned up")
        except Exception as e:
            print(f"Error during cleanup: {e}")

def main():
    emulator = USBGadgetEmulator()
    
    # Requires sudo/root permissions
    if os.geteuid() != 0:
        print("This script must be run as root")
        return

    # Create virtual disk
    if not emulator.create_disk_image():
        return

    # Setup USB Gadget
    if not emulator.setup_gadget():
        return

    try:
        # Keep script running
        input("Press Enter to stop the USB Gadget...")
    finally:
        emulator.cleanup()

if __name__ == '__main__':
    main()
