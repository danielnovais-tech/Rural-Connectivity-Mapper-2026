# Google Forms Integration Guide

## Overview

This guide explains how to use **Google Forms** as an alternative submission method for collecting rural connectivity data from non-technical users. Google Forms provides an easy-to-use web interface that doesn't require any programming knowledge.

## Why Use Google Forms?

- ✅ **User-Friendly** - Simple web form interface, no technical knowledge required
- ✅ **Mobile Compatible** - Works on smartphones for field data collection
- ✅ **Free** - No cost for basic usage
- ✅ **Automatic Storage** - Responses automatically saved to Google Sheets
- ✅ **CSV Export** - Easy export to CSV for import into Rural Connectivity Mapper
- ✅ **Shareable** - Send link via email, WhatsApp, or social media
- ✅ **Offline Mode** - Can work offline with Google Forms mobile app

## Prerequisites

- Google Account (free Gmail account)
- Access to Google Forms (forms.google.com)
- Basic knowledge of CSV file handling

---

## Step 1: Create Your Google Form

### 1.1 Access Google Forms

1. Go to [forms.google.com](https://forms.google.com)
2. Sign in with your Google Account
3. Click **+ Blank** to create a new form

### 1.2 Configure Form Settings

1. Click the **Settings** gear icon (⚙️) at the top right
2. Under **Responses**:
   - ✅ Check "Collect email addresses" (optional, for tracking)
   - ✅ Check "Limit to 1 response" (optional, to prevent duplicates)
3. Click **Save**

---

## Step 2: Add Form Fields

Create the following fields in your form to match the CSV import format:

### Required Fields

#### Field 1: City/Location Name
- **Question Type:** Short answer
- **Question:** "City or Location Name"
- **Description:** "Enter the name of the city or rural area"
- **Required:** ✅ Yes
- **Example:** São Paulo, Brasília, Rural Area - Goiás

#### Field 2: Internet Service Provider
- **Question Type:** Dropdown or Short answer
- **Question:** "Internet Service Provider"
- **Description:** "Name of your ISP (e.g., Starlink, Claro, Vivo, TIM)"
- **Required:** ✅ Yes
- **Dropdown Options (recommended):**
  - Starlink
  - Viasat
  - HughesNet
  - Claro
  - Vivo
  - TIM
  - Oi
  - Various
  - Other (please specify)

#### Field 3: Latitude
- **Question Type:** Short answer
- **Question:** "Latitude"
- **Description:** "GPS latitude coordinate (e.g., -23.5505). Use Google Maps to find coordinates."
- **Validation:** Number, between -90 and 90
- **Required:** ✅ Yes

#### Field 4: Longitude
- **Question Type:** Short answer
- **Question:** "Longitude"
- **Description:** "GPS longitude coordinate (e.g., -46.6333). Use Google Maps to find coordinates."
- **Validation:** Number, between -180 and 180
- **Required:** ✅ Yes

#### Field 5: Download Speed
- **Question Type:** Short answer
- **Question:** "Download Speed (Mbps)"
- **Description:** "Internet download speed in Mbps. Use speedtest.net to measure."
- **Validation:** Number, greater than 0
- **Required:** ✅ Yes

#### Field 6: Upload Speed
- **Question Type:** Short answer
- **Question:** "Upload Speed (Mbps)"
- **Description:** "Internet upload speed in Mbps. Use speedtest.net to measure."
- **Validation:** Number, greater than 0
- **Required:** ✅ Yes

#### Field 7: Latency/Ping
- **Question Type:** Short answer
- **Question:** "Latency/Ping (ms)"
- **Description:** "Internet latency in milliseconds. Use speedtest.net to measure."
- **Validation:** Number, greater than 0
- **Required:** ✅ Yes

### Optional Fields

#### Field 8: Jitter (Optional)
- **Question Type:** Short answer
- **Question:** "Jitter (ms)"
- **Description:** "Jitter in milliseconds (optional, default: 0)"
- **Validation:** Number, greater than or equal to 0
- **Required:** ❌ No
- **Default:** 0

#### Field 9: Packet Loss (Optional)
- **Question Type:** Short answer
- **Question:** "Packet Loss (%)"
- **Description:** "Packet loss percentage (optional, default: 0)"
- **Validation:** Number, between 0 and 100
- **Required:** ❌ No
- **Default:** 0

---

## Step 3: Customize Your Form

### Add Form Title and Description

1. Click on the form title (default: "Untitled form")
2. Enter: **"Rural Connectivity Data Collection"**
3. Add description:
   ```
   Help us map rural internet connectivity in Brazil! Please measure your internet 
   speed using speedtest.net and fill in the information below. Your data will 
   contribute to improving rural connectivity infrastructure.
   ```

### Add Helpful Instructions

At the top of the form, add a section with instructions:

1. Click **+** to add a new question
2. Select **Short answer** type
3. Change to **Title and description** (from the menu)
4. Add:
   ```
   📍 How to Find Your Coordinates:
   1. Open Google Maps
   2. Right-click on your location
   3. Click the coordinates at the top to copy them
   
   🌐 How to Measure Your Speed:
   1. Go to speedtest.net
   2. Click "Go" to run the test
   3. Note down Download, Upload, and Latency values
   ```

---

## Step 4: Test Your Form

1. Click **Preview** (eye icon) at the top right
2. Fill out the form with test data
3. Submit the form
4. Verify data appears in the Responses tab

---

## Step 5: Share Your Form

### Get the Form Link

1. Click **Send** button at the top right
2. Click the **Link** icon (🔗)
3. Click **Copy** to copy the form URL
4. Share this link with users via:
   - Email
   - WhatsApp
   - Social media
   - SMS
   - QR code (click "Shorten URL" for QR code option)

### Embed in Website (Optional)

1. Click **Send** → **Embed HTML** (`<>` icon)
2. Copy the HTML code
3. Paste into your website

---

## Step 6: Collect Responses

Responses are automatically saved to Google Forms and can be viewed in real-time:

1. Open your form
2. Click **Responses** tab
3. View summary charts or individual responses

---

## Step 7: Export Data to CSV

### 7.1 Create Google Sheets Spreadsheet

1. In your form, click **Responses** tab
2. Click the **Google Sheets** icon (green spreadsheet icon)
3. Select "Create a new spreadsheet"
4. Click **Create**

This automatically creates a Google Sheets spreadsheet linked to your form.

### 7.2 Prepare Data for Export

The Google Sheets will have columns like:
- Timestamp
- City/Location Name
- Internet Service Provider
- Latitude
- Longitude
- Download Speed (Mbps)
- Upload Speed (Mbps)
- Latency/Ping (ms)
- Jitter (ms)
- Packet Loss (%)

### 7.3 Format the Spreadsheet

To match the expected CSV format, you need to:

1. **Add/Rename Headers** - Ensure the first row has these exact headers:
   ```
   id,city,provider,latitude,longitude,download,upload,latency,jitter,packet_loss,timestamp
   ```

2. **Add ID Column** - Insert a column at the beginning with sequential IDs (1, 2, 3, ...)

3. **Rename Columns** to match expected format:
   - "City/Location Name" → "city"
   - "Internet Service Provider" → "provider"
   - "Download Speed (Mbps)" → "download"
   - "Upload Speed (Mbps)" → "upload"
   - "Latency/Ping (ms)" → "latency"
   - "Jitter (ms)" → "jitter"
   - "Packet Loss (%)" → "packet_loss"

4. **Format Timestamp** - Ensure timestamp is in ISO 8601 format: `2026-01-15T10:30:00`

### 7.4 Export to CSV

1. In Google Sheets, click **File** → **Download** → **Comma Separated Values (.csv)**
2. Save the file (e.g., `connectivity_data.csv`)

---

## Step 8: Import Data into Rural Connectivity Mapper

### 8.1 Verify CSV Format

Your CSV should look like this:

```csv
id,city,provider,latitude,longitude,download,upload,latency,jitter,packet_loss,timestamp
1,São Paulo,Starlink,-23.5505,-46.6333,165.4,22.8,28.5,3.2,0.1,2026-01-15T10:30:00
2,Brasília,Claro,-15.7801,-47.9292,92.1,15.3,38.7,6.5,0.8,2026-01-15T11:00:00
```

### 8.2 Import Using CLI

```bash
python main.py --importar connectivity_data.csv
```

### 8.3 Generate Reports

After importing, you can generate reports, maps, and analysis:

```bash
# Generate HTML report
python main.py --relatorio html

# Create interactive map
python main.py --map

# Analyze temporal trends
python main.py --analyze

# Complete workflow
python main.py --importar connectivity_data.csv --map --analyze --relatorio html
```

---

## Complete Workflow Example

```
1. Create Google Form → 2. Share with users → 3. Collect responses → 
4. Export to Google Sheets → 5. Format columns → 6. Download CSV → 
7. Import to mapper → 8. Generate reports/maps
```

---

## Sample Google Forms Template

**Quick Start:** Use this pre-configured template (copy and customize):

### Form Structure

```
═══════════════════════════════════════════════════
   RURAL CONNECTIVITY DATA COLLECTION FORM
═══════════════════════════════════════════════════

📋 Instructions:
Please measure your internet speed at speedtest.net and 
provide your location coordinates from Google Maps.

───────────────────────────────────────────────────

1. City or Location Name *
   [Short answer text field]

2. Internet Service Provider *
   [Dropdown]
   ○ Starlink
   ○ Viasat
   ○ HughesNet
   ○ Claro
   ○ Vivo
   ○ TIM
   ○ Oi
   ○ Other

3. Latitude (GPS Coordinate) *
   [Number: -90 to 90]
   Hint: Right-click on Google Maps to get coordinates

4. Longitude (GPS Coordinate) *
   [Number: -180 to 180]

5. Download Speed (Mbps) *
   [Number: > 0]
   Measure at speedtest.net

6. Upload Speed (Mbps) *
   [Number: > 0]

7. Latency/Ping (ms) *
   [Number: > 0]

8. Jitter (ms) - Optional
   [Number: ≥ 0]

9. Packet Loss (%) - Optional
   [Number: 0-100]

───────────────────────────────────────────────────
[Submit] button
═══════════════════════════════════════════════════
```

---

## Troubleshooting

### Common Issues

**Issue:** Coordinates not validating
- **Solution:** Ensure latitude is between -90 and 90, longitude between -180 and 180
- Use decimal format (e.g., -23.5505, not degrees/minutes/seconds)

**Issue:** CSV import fails
- **Solution:** Verify column headers match exactly: `id,city,provider,latitude,longitude,download,upload,latency,jitter,packet_loss,timestamp`
- Check for special characters or extra spaces in headers

**Issue:** Missing required fields
- **Solution:** Ensure all required fields are filled in Google Form
- Set fields as "Required" in Google Forms settings

**Issue:** Invalid timestamp format
- **Solution:** Convert timestamp to ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`
- Example: `2026-01-15T10:30:00`

**Issue:** Duplicate entries
- **Solution:** Enable "Limit to 1 response" in form settings
- Manually remove duplicates in Google Sheets before export

---

## Data Privacy Considerations

- 🔒 **Anonymous Collection** - Don't require personal information unless necessary
- 🔒 **Secure Storage** - Google Forms data is stored securely by Google
- 🔒 **Access Control** - Only share form links with authorized users
- 🔒 **Data Retention** - Set up automatic data deletion if needed
- 🔒 **Compliance** - Follow LGPD (Brazil) and GDPR regulations if applicable

---

## Advanced Features

### Conditional Logic

Use form sections and conditional logic to show/hide fields based on responses:

1. Add section breaks
2. Click "⋮" (three dots) on a question → "Go to section based on answer"
3. Set up conditional flows

### Email Notifications

Get notified when someone submits the form:

1. In Google Sheets, click **Tools** → **Notification rules**
2. Select "A user submits a form"
3. Choose notification frequency

### Automated Import (Advanced)

For advanced users, consider:
- Google Sheets API to fetch data programmatically
- Apps Script to auto-format responses
- Scheduled exports using Google Apps Script triggers

---

## Quick Reference: Sample Data

For testing purposes, we've included a sample Google Forms export CSV file:

**Location:** `docs/sample_google_forms_export.csv`

This file contains 6 sample connectivity points from different Brazilian cities demonstrating the proper format for Google Forms exports. You can use this as a reference for formatting your own exports.

**Test the import:**
```bash
python main.py --importar docs/sample_google_forms_export.csv
python main.py --map --relatorio html
```

---

## Support Resources

- **Google Forms Help:** [support.google.com/forms](https://support.google.com/forms)
- **Finding Coordinates:** [support.google.com/maps](https://support.google.com/maps)
- **Speed Testing:** [speedtest.net](https://www.speedtest.net/)
- **Project Issues:** [GitHub Issues](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues)

---

## Comparison: Google Forms vs. Direct CSV vs. API

| Feature | Google Forms | Direct CSV | API (Future) |
|---------|-------------|------------|--------------|
| **Technical Skills** | None required | Basic file editing | Programming knowledge |
| **User Interface** | Web form | Text editor/Excel | API client |
| **Mobile Friendly** | ✅ Excellent | ❌ Difficult | ⚠️ Depends on client |
| **Real-time Entry** | ✅ Yes | ❌ No | ✅ Yes |
| **Offline Support** | ⚠️ Limited | ✅ Yes | ❌ No |
| **Validation** | ✅ Built-in | ❌ Manual | ✅ Built-in |
| **Best For** | Non-technical users, field collection | Bulk data import | Automated systems |

---

## Conclusion

Google Forms provides an excellent **alternative submission method** for users who are not comfortable with CSV files or APIs. It's particularly useful for:

- **Field data collection** using mobile devices
- **Community participation** in rural connectivity mapping
- **Non-technical stakeholders** contributing data
- **Quick deployments** without infrastructure setup

Once data is collected via Google Forms, it seamlessly integrates with the Rural Connectivity Mapper's existing CSV import functionality.

---

**📧 Questions?** Open an issue on [GitHub](https://github.com/danielnovais-tech/Rural-Connectivity-Mapper-2026/issues)

**🌍 Happy Mapping!** Help improve rural connectivity in Brazil! 🇧🇷
