To avoid errors, the suggested order to run these files in is below.

1. **OCR.py** -- extract text from all images
2. **get_screenshots.py**  -- get info about which images are screenshots
3. **add_risk.py** -- add info about which images are risky
4. **add_metadata.py** -- add info about other metadata features
5. **classification.py** -- perform the classification

**Steps 1-4 have already been completed.** Output of these stages has been sent to Feature_Output.json.

**Feature_Output.json** contains the  metadata information for all images.
The message and image count features reflect the number of messages in the conversation up to that point,
and this allows for risk detection in the moment as soon as a message has been sent.

Reference Paper: Ali, S., Razi, A., Seunghyun, K., Alsoubai, A., Gracie, J., De Choudhury, M., ... & Stringhini, G. (2022). Understanding the Digital Lives of Youth: Analyzing Media Shared within Safe Versus Unsafe Private Conversations on Instagram.
