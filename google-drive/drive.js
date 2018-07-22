var url = new java.net.URL(execution.getVariable("urlVar"));
//var url = new java.net.URL(${url});
var boundary = "###############################################";
var crlf = "\r\n";
var twoHyphens = "--";

var httpConn = url.openConnection();
httpConn.setUseCaches(false);
httpConn.setDoOutput(true);
httpConn.setDoInput(true);

httpConn.setRequestMethod("POST");
httpConn.setRequestProperty("Connection", "Keep-Alive");
httpConn.setRequestProperty("Cache-Control", "no-cache");
httpConn.setRequestProperty(
  "Content-Type", "multipart/form-data;boundary=" + boundary);

var request =  new java.io.DataOutputStream(httpConn.getOutputStream());

var uploadFile = execution.getVariableTyped(execution.getVariable("fileUploadVar"));
//var uploadFile = execution.getVariableTyped(${file});

var fileName = uploadFile.getFilename();
var fieldName = "file";
request.writeBytes(twoHyphens + boundary + crlf);
request.writeBytes("Content-Disposition: form-data; name=\"" +
                   fieldName + "\";filename=\"" +
                   fileName + "\"" + crlf);
request.writeBytes(crlf);

var fileData = uploadFile.getValue();
org.apache.commons.io.IOUtils.copy(fileData, httpConn.getOutputStream());
var response ="";

request.writeBytes(crlf);
request.writeBytes(twoHyphens + boundary + twoHyphens + crlf);

request.flush();
request.close();

var status = httpConn.getResponseCode();
if (status == java.net.HttpURLConnection.HTTP_OK) {
  httpConn.disconnect();
}
