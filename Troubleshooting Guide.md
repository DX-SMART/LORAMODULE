# DX-SMART LoRa Module Troubleshooting Guide

If you encounter problems while using or flashing the LoRa module, please follow the steps below for troubleshooting.

---

## Step 1: Confirm the Development Board Version

Please first confirm your development board version:

* **PJ23**
* **PJ26**

Different versions use different RTS/DTR control modes.

<img width="1266" height="558" alt="WPS圖片(1)" src="https://github.com/user-attachments/assets/355335d5-9803-4572-9973-68eb967d96ec" />

---

## Step 2: Configure MCUISP

Open the **MCUISP** software and confirm the following settings:

1. Click `EnumPort` to automatically detect the serial port
2. Select the correct COM port
3. Set baud rate to `460800`
4. Load the correct `.hex` firmware file（If you cannot find the .hex file, please check the path shown in the image to make sure it matches.）
5. Configure RTS/DTR settings:

### PJ23:

```text id="6g3kpr"
Reset@DTR Low(<-3V), ISP@RTS High
```

### PJ26:

```text id="1mvx9d"
Reset@DTR High(>+3V), ISP@RTS Low
```

<img width="841" height="962" alt="wechat_2026-05-28_110105_842" src="https://github.com/user-attachments/assets/e12a1f38-ef8b-4fcd-a69b-1bb2fdc51284" />
<img width="1343" height="740" alt="image" src="https://github.com/user-attachments/assets/b77b7ff8-9777-494a-b18d-32712869c67e" />

---

## Step 3: Read Chip Information

1. Click:

```text id="0qk4hc"
Read ChipInfo(R)
```

2. Immediately press the `RST` button on the development board.

### Result:

* If the chip information is successfully read → Settings are correct
* If it fails → Continue to Step 4

<img width="864" height="648" alt="image" src="https://github.com/user-attachments/assets/563c3fa0-863e-4e11-adec-da816c91604d" />

<img width="667" height="737" alt="image" src="https://github.com/user-attachments/assets/7f9cd1de-5336-4645-aa5b-fd5b58381637" />

---

## Step 4: Serial Port Test

Use a serial port debugging tool to check whether the module is running normally.

### Serial Port Parameters:

```text id="k7s2lb"
Baud Rate: 9600
Data Bits: 8
Stop Bits: 1
Parity: NONE
```

Press the `RST` button and observe the serial output.

---

### Case A: Output Detected

Example:

```text id="g2zp4v"
---> Power On
---> V1.2.35
---> DX SX1262...
```

This means the module firmware is running normally.

Please check:

* MCUISP configuration
* RTS/DTR settings
* USB cable

<img width="554" height="617" alt="image" src="https://github.com/user-attachments/assets/68bae577-4a2e-47dd-93d2-46d51a341ec1" />

---

### Case B: No Output

If there is absolutely no response after pressing `RST`:

* The chip may not contain firmware
* RTS/DTR settings may be incorrect
* Wrong board type may be selected

Please recheck the PJ23 / PJ26 configuration carefully.

---

# 📞 Contact Us

If the issue still cannot be resolved, please provide the following information:

1. LoRa module model
2. Development board version (PJ23 / PJ26)
3. Detailed problem description
4. Computer operating system (Windows/macOS)
5. High-resolution error screenshots, operation videos, or serial port output screenshots (this will help us identify the issue more quickly)

---
Email: manager@szdx-smart.com
WhatsApp: +86 15798463070

