# NiteStart

There is a reason why laptop to laptop USB connection was unheard of and why we have never seen anyone even try to do it
Most laptop USB controllers are designed to act as Hosts only not to be controlled.  

The kernal of most distros including GNU and Debian along with all Standard versions of Windows do not allow USB Gadget  

It is a fundamental feature build into the kernal itself.  

So for NiteStart to work  
We either need a custom compiled kernal with USB Gadget support (kinda kills the whole practical utility of NiteStart)  
Or  
Different hardware like a Raspberry Pi or Android Device that supports OTG and can be rooted  


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

![image](https://github.com/user-attachments/assets/4d4a37e7-e354-4f78-8d10-3f22b60abf9a)  
This is where the hardware limitation was discovered.
