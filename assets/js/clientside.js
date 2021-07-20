window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientsideSigma: {
        tabChangeFigRender: function(rawData, oversamplingData, switchValue=[false]) {
            let data = [];
            let layout = {
                "xaxis": {"tick0": -2, "dtick": 1,
                          "type": "log", "title": {"text": "Time (s)"}, 
                          "ticks": "outside" 
                },
                "yaxis": {"title": {"text" : "G(t) (Pa)"}, "range": [0, 1.0],
                          "rangemode": "tozero", "ticks": "outside"
                },
            }
            let rawDataTrace = {
                "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
                "name": "Experiental Data",
                "mode": "markers",
                "marker": {"symbol": "circle-open", 
                           "size": 10, "maxdisplayed": 200},
                "x": rawData.x,
                "y": rawData.y
            }

            /**
            * Only oversampling button on and oversamplingData has value to render Oversamping figure.
            * You may feel wired about the switchValue is [bool] not bool.
            * It's the Dash's wired part... Just follow the framework's rule.
            */
            if (switchValue[0] == true && oversamplingData != undefined) {
                console.log("========= in oversampling =======");
                // console.log(oversamplingData)
                // data = oversamplingData;
                let oversamplingDataTrace = {
                    "name": "Oversamping Data",
                    "mode": "markers",
                    "marker": {"symbol": "circle-x", 
                                "size": 6, "maxdisplayed": 200},
                    "x": oversamplingData.x,
                    "y": oversamplingData.y
                }
                
                data.push(rawDataTrace, oversamplingDataTrace);
            } else {
                console.log("========= in sigma =============");
                // console.log(rawData)
                // data = rawData;
                data.push(rawDataTrace);
            }
    
            return {
                "data" : data,
                "layout": layout
            }   
        }
    }
});