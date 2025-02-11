# NiteStart
```
# Initial setup commands
sudo modprobe libcomposite
cd /sys/kernel/config/usb_gadget/
mkdir -p nitestart
cd nitestart
```
![image](https://github.com/user-attachments/assets/757ecbef-9f5c-48fe-ac74-a2e16a6cfa63)  

```
# Configure USB Device Parameters
echo 0x1d6b > idVendor   # Linux Foundation
echo 0x0104 > idProduct  # Multifunction Composite Gadget
echo 0x0100 > bcdDevice  # Device version
echo 0x0200 > bcdUSB     # USB 2.0 specification
```
```
# Run these commands on your Linux laptop
ls /sys/kernel/config/usb_gadget
# If this shows a directory, USB Gadget is supported
```
