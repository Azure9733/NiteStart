# NiteStart
```
# Initial setup commands
sudo modprobe libcomposite
cd /sys/kernel/config/usb_gadget/
mkdir -p nitestart
cd nitestart

# Configure USB Device Parameters
echo 0x1d6b > idVendor   # Linux Foundation
echo 0x0104 > idProduct  # Multifunction Composite Gadget
echo 0x0100 > bcdDevice  # Device version
echo 0x0200 > bcdUSB     # USB 2.0 specification
```
