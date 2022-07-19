
var methodName      = srcMethods.data['methodName']
var applicable      = srcMethods.data['applicable']
var minTemp         = srcDef.data['minTemp']
var maxTemp         = srcDef.data['maxTemp']
var minPH           = srcDef.data['minPH']
var maxPH           = srcDef.data['maxPH']
var worksAerobic    = srcDef.data['worksAerobic']
var worksAnaerobic  = srcDef.data['worksAnaerobic']
const Temperature   = sl2.value
const pH            = sl1.value
const milieu        = rG1.active

// go through temperature condition
for (var i = 0; i < minTemp.length; i++) {
    var myStr = ''
    if (Temperature > minTemp[i] && Temperature < maxTemp[i]) {
        myStr += 'x'
    } else {
        myStr += 'o'
    }
    if (pH > minPH[i] && pH < maxPH[i]) {
        myStr += 'x'
    } else {
        myStr += 'o'
    }
    if (milieu == 0 && worksAerobic[i] == "yes") {
        myStr += 'x'
    } else if (milieu == 1 && worksAnaerobic[i] == "yes") {
        myStr += 'x'
    } else {
        myStr += 'o'
    }
    applicable[i] = myStr
}

srcMethods.data['methodName'] = methodName
srcMethods.data['applicable'] = applicable

srcMethods.change.emit();