window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientsideSigma: {
        tabChangeFigRender: function(rawData, oversampingData, switchValue=[false]) {
            let data = [];
            let layout = {
                "xaxis": {"dtick": 1, "tick0": -2, "type": "log", "title": {"text": "Time (s)"}},
                "yaxis": {"title": {"text" : "G(t) (Pa)"}},
            }
            let rawDataTrace = {
                "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
                "name": "Experiental Data",
                "mode": "markers",
                "marker": {"symbol": "circle-open", "size": 12},
                "x": rawData.x,
                "y": rawData.y
            }

            /**
            * Only oversamping button on and oversampingData has value to render Oversamping figure.
            * You may feel wired about the switchValue is [bool] not bool.
            * It's the Dash's wired part... Just follow the framework's rule.
            */
            if (switchValue[0] == true && oversampingData != undefined) {
                // console.log("========= in oversamping =======");
                // console.log(oversampingData)
                // data = oversampingData;
                let oversampingDataTrace = {
                    "name": "Oversamping Data",
                    "mode": "markers",
                    "marker": {"symbol": "circle-x", "size": 6},
                    "x": oversampingData.x,
                    "y": oversampingData.y
                }
                
                data.push(rawDataTrace, oversampingDataTrace);
            } else {
                // console.log("========= in sigma =============");
                // console.log(rawData)
                // data = rawData;
                data.push(rawDataTrace);
            }
    
            return {
                "data" : data,
                "layout": layout
            }   
        }
    },
    clientsideFT:{
        tabChangeFigRender: function(ftData, oversampledftData, switchValue=[false]) {
            let data = [];
            let layout = {
                "xaxis": {"dtick": 1, "tick0": -12, "type": "log", "title": {"text": "ω [rad/s])"}},
                "yaxis": {"dtick": 1, "tick0": -7, "type": "log", "title": {"text" : "G′ G′′ [Pa ]"}},
            }
            let ftDataTrace0 = {
                "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
                "name": "FT Data0",
                "mode": "lines",
                "marker": {"symbol": "circle-open", "size": 12},
                "x": ftData.x,
                "y": ftData.y1,
            }
            // let ftDataTrace1 = {
            //     "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
            //     "name": "FT Data1",
            //     "mode": "markers",
            //     "marker": {"symbol": "circle-open", "size": 12},
            //     "x": ftData.x,
            //     "y": ftData.y2,
            // }

            /**
            * Only oversamping button on and oversampingData has value to render Oversamping figure.
            * You may feel wired about the switchValue is [bool] not bool.
            * It's the Dash's wired part... Just follow the framework's rule.
            */
            if (switchValue[0] == true && oversampledftData != undefined) {
                console.log("========= in ft oversamping =======");
                // console.log(oversampingData)
                // data = oversampingData;
                let oversampledftDataTrace0 = {
                    "name": "OversampledftData0",
                    "mode": "lines",
                    "marker": {"symbol": "circle-x", "size": 6},
                    "x": oversampledftData.x,
                    "y": oversampledftData.y1,
                }
                let oversampledftDataTrace1 = {
                    "name": "OversampledftData1",
                    "mode": "markers",
                    "marker": {"symbol": "circle-x", "size": 6},
                    "x": oversampledftData.x,
                    "y": oversampledftData.y2,
                }
                
                data.push(oversampledftDataTrace0, oversampledftDataTrace1);
            } else {
                console.log("========= in ft =============");
                // console.log(rawData)
                // data = rawData;
                // data.push(ftDataTrace0, ftDataTrace1);
                data.push(ftDataTrace0);  
            }
            
            console.log(ftData.x.slice(0, 20))
            console.log(ftData.y1.slice(0, 20))

            return {
                "data" : data,
                "layout": layout
            }   
        }
    }
});