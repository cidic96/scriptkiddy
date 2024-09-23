/**
 * Combines data from all sheets in the current spreadsheet.
 * @return The combined data from all sheets.
 * @customfunction
 */
function combineAllSheets() {
  // Get the active spreadsheet
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheets = ss.getSheets();
  var combinedData = [];

  // Iterate through all sheets
  for (var i = 0; i < sheets.length; i++) {
    var sheet = sheets[i];
    var sheetName = sheet.getName();
    
    var data = sheet.getDataRange().getValues();
    
    // Add sheet name as the first row
    combinedData.push([sheetName]);
    
    // Add the data from the current sheet
    for (var j = 0; j < data.length; j++) {
      combinedData.push(data[j]);
    }
    
    // Add an empty row between sheets
    combinedData.push([]);
  }

  return combinedData;
}