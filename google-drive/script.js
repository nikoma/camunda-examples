with (new JavaImporter(org.jsoup))
{

  // var body = {
  //   "myKey1": "myValue1",
  //   "myKey2": "myValue2",
  //   "myKey3": {
  //     "internal1":"internalV1",
  //     "internal2":"internalV2"
  //     },
  //   "myKey4": [
  //     1,2,3,4,5
  //     ]
  // }

  var doc = Jsoup.connect('http://date.jsontest.com')
                  .method(Java.type('org.jsoup.Connection.Method').GET)
                  // .method(Java.type('org.jsoup.Connection.Method').POST)
                  .header('Accept', 'application/json')
                  .header('Content-Type', 'application/json')
                  // .data('filterABC', 'subgroup1')
                  // .requestBody(JSON.stringify(body))
                  .timeout(30000)
                  .ignoreContentType(true) // This is used because Jsoup "approved" content-types parsing is enabled by default by Jsoup
                  .execute()

  var resBody = doc.body()
  var resStatusCode = doc.statusCode()
  var resStatusMessage = doc.statusMessage()
  var resContentType = doc.contentType()
  var resCharSet = doc.charset()

}

function spinify(body)
{
  var parsed = JSON.parse(body)
  var stringified = JSON.stringify(parsed)
  var spin = S(stringified)
  return spin
}

execution.setVariable('responseBodyString', spinify(resBody))
