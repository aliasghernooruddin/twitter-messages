var cityTimezones = require('city-timezones');
var moment = require('moment-timezone');

const prompt = require("prompt-sync")({ sigint: true });

var run = true

while (run) {
    const name = prompt("Enter City/Country, X to exit: ");

    if (name == 'x' || name == 'X') {
        run = false
    } else {
        const cityLookup = cityTimezones.lookupViaCity(name)
        for (let i of cityLookup) {
            let time = moment().tz(i.timezone).format('hh:mm:ss A Z')
            console.log(`Timezone: ${i.timezone}`)
            console.log(`Current Time is: ${time}`)
            console.log("\n")
        }
    }

}

