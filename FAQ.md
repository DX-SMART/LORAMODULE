
# LoRa Modules

## LORA-001 — Firmware Upgrade

**Q: Can I upgrade the LoRa module firmware by myself?**

**A:** No. The LoRa module does not support user-side firmware upgrades.

If a firmware upgrade is required, please contact us and return the module to our company. Our technical team will perform the firmware upgrade.


---

## LORA-002 — Arduino / ESP32 Compatibility

**Q: Can the LoRa module be used with Arduino or ESP32?**

**A:** Yes. Our LoRa modules can be used with Arduino and ESP32. However, the application code needs to be developed by the customer.

We currently do not provide programming or development support for Arduino or ESP32.

For some non-development modules, such as **LR01, LR22, and LR32**, Arduino examples are available for reference.


---

## LORA-003 — Frequency Band Configuration

**Q: Can the LR20 / LR30 frequency band be changed?**

**A:** Yes. The **LR20 and LR30** support changing the operating frequency band through programming.

The supported frequency ranges are:

| Version | Frequency Range |
|---|---|
| 433 version | 433–470 MHz |
| 900 version | 850–930 MHz |

Please refer to the product documentation for the detailed supported frequency bands.


---

## LORA-004 — Programming Failure

**Q: What should I do if programming fails?**

**A:** If the program cannot be successfully flashed to the device, you can try using an **ST-Link** to reprogram the device firmware.


---

## LORA-005 — Mobile Phone Operation

**Q: Can I operate the LoRa module directly from a mobile phone?**

**A:** No. The LoRa module cannot directly communicate with a mobile phone, so it cannot be directly operated through a phone.

---

## LORA-006 – Original Factory Firmware Location

**Q: Where can I find the original factory firmware (HEX file) to restore the device?**

**A:** You can find the original factory firmware (`DX_TESET.hex`) inside the provided resource package. Unzip the package and navigate to the following path:

`07 Programming code demonstration` -> `LR20&30-900` -> `LR20&30-900` -> `Project` -> `Objects`

Inside the **Objects** folder, locate **`DX_TESET.hex`** and re-flash it onto the MCU (STM32F103C8T6) using an **ST-Link**, **J-Link**, or **Serial ISP tool** to restore the default factory settings.
<img width="696" height="625" alt="image" src="https://github.com/user-attachments/assets/16856f6c-1e94-4ce7-89de-92f833f0a1fd" />




