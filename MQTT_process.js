window.onload = function() {
    let dataLength = 700
    let ecgFromArduinoTopic = "iotsystem/heartcare/ecg/display/"
    let ecgFromPhysionetTopic = "iotsystem/heartcare/ecg/physionet/display/"
    let warningTopic = "iotsystem/heartcare/warning/display/"
    var client = mqtt.connect('wss://m14.cloudmqtt.com',{
        port: 36649,
        username: "chvnbmzq",
        password: "nE_X6pIBl1kx"
      })

      client.on('connect', function () {
        console.log("connected")
      })

      client.subscribe(ecgFromArduinoTopic)
      client.subscribe(ecgFromPhysionetTopic)
      client.subscribe(warningTopic)

      client.on("message", function (topic, payload) {
          if(topic == ecgFromArduinoTopic){
            processEcgFromArduino(topic, payload)
          }
          else if(topic == ecgFromPhysionetTopic){
              processEcgFromPhysionet(topic, payload)
          }
          else if(topic ==warningTopic){
              processWarning(topic, payload)
          }
      })

     function processEcgFromPhysionet(topic, payload){
        content= payload.toString()
        strData = content.split(',')
        data = strData.map( x => parseInt(x))
        if(data.length == 100){
            updateChart(100, data)
        }
    }
     function processEcgFromArduino(topic, payload){
        content = payload.toString().substring(1)
        // if(content.length == 200){
        //   contentDecode = decodeContent(content)
        //   updateChart(100, contentDecode)
        // }
        data = content.split(',').map(x=> parseInt(x))
        if(data.length == dataLength){
            updateChart(dataLength, data)    
        }
      }

    // [Obsolete]
     function decodeContent(content){
       result = []
       for(i=0; i<content.length; i=i+2){
        num = (content[i].charCodeAt())*94 + content[i+1].charCodeAt()
        result.push(num)
       }
       return result
     }

     function processWarning(topic, payload){
         content = payload.toString();
         console.log(content);
         data = content.split(',').map(x => parseInt(x))
         updateChartWarning(data)
     }
}