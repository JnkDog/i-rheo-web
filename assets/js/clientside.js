// Function implementation list
gammaRender = function(rawData, oversamplingData, switchValue=[false]) {
    if (rawData == undefined) {
        return;
    }

    let data = [];
    let layout = {
        "xaxis": {"tick0": -2, "dtick": 1,
                "type": "log", "title": {"text": "Time [s]"}, 
                "ticks": "outside" 
        },
        "yaxis": {"title": {"text" : "γ [-]"}, 
                // "range": [0, 1.0],
                "rangemode": "tozero", "ticks": "outside"
        },
    }
    let rawDataTrace = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "Experiental Data",
        "mode": "markers",
        "marker": {color:"orange", "symbol": "circle-open", 
                "size": 10, "maxdisplayed": 200},
        "x": rawData.x,
        "y": rawData.z
    }

    /**
    * Only oversampling button on and oversamplingData has value to render Oversampling figure.
    * You may feel wired about the switchValue is [bool] not bool.
    * It's the Dash's wired part... Just follow the framework's rule.
    */
    if (switchValue[0] == true && oversamplingData != undefined) {
        // console.log("========= in oversampling =======");
        // console.log(oversamplingData)
        // data = oversamplingData;
        let oversamplingDataTrace = {
            "name": "Oversampling Data",
            "mode": "markers",
            "marker": {"symbol": "circle-x", 
                        "size": 6, "maxdisplayed": 200},
            "x": oversamplingData.x,
            "y": oversamplingData.z
        }
        
        data.push(rawDataTrace, oversamplingDataTrace);
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

motAtRender = function(rawData, oversamplingData, switchValue=[false]) {
    if (rawData == undefined) {
        return;
    }

    let data = [];
    let layout = {
        "xaxis": {"tick0": -2, "dtick": 1,
                "type": "log", "title": {"text": "t (sec)"}, 
                "ticks": "outside" 
        },
        "yaxis": {"title": {"text" : "A(t)"}, 
                // "range": [0, 1.0],
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

    if (switchValue[0] == true && oversamplingData != undefined) {
    let oversamplingDataTrace = {
        "name": "Oversampling Data",
        "mode": "markers",
        "marker": {"symbol": "circle-x", 
                    "size": 6, "maxdisplayed": 200},
        "x": oversamplingData.x,
        "y": oversamplingData.y
    }

    data.push(rawDataTrace, oversamplingDataTrace);
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

motRender = function(ftData, oversampledftData, switchValue=[false]) {
    if (ftData == undefined) {
        return;
    }

    let data = [];
    let layout = {
        "xaxis": {"dtick": 1, "tick0": -12, 
                  "type": "log", "title": {"text": "Frequency (Hz)"},
                  "ticks": "outside"},
        "yaxis": {"dtick": 1, "tick0": -7, 
                  "type": "log", "title": {"text" : "Moduli (Pa)"},
                  "ticks": "outside"},
        // "colorway": ["green"],
    }
    let ftDataTrace0 = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "G'",
        "mode": "lines",
        "line": {color:"black"},
        "x": ftData.x,
        "y": ftData.y1,
    }
    let ftDataTrace1 = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "G''",
        "mode": "lines",
        "line": {color:"red"},
        "x": ftData.x,
        "y": ftData.y2,
    }

    if (switchValue[0] == true && oversampledftData != undefined) {
        let oversampledftDataTrace0 = {
            "name": "Oversampled-G'",
            "mode": "lines",
            "line": {color:"black"},
            "x": oversampledftData.x,
            "y": oversampledftData.y1,
        }
        let oversampledftDataTrace1 = {
            "name": "Oversampled-G''",
            "mode": "lines",
            "line": {color:"red"},
            "x": oversampledftData.x,
            "y": oversampledftData.y2,
        }
        
        data.push(oversampledftDataTrace0, oversampledftDataTrace1);
    } else {
        data.push(ftDataTrace0, ftDataTrace1);  
    }

    return {
        "data" : data,
        "layout": layout
    }   
}

uploadMessageRecovery = function(rawData) {
    if (rawData == undefined) {
        return;
    }

    const filename = rawData.filename;
    const len    = rawData.lines;

    return `The upload file ${filename} 
            with ${len} lines`;
}

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientsideSigma: {
        tabChangeFigRender: function(rawData, oversamplingData, switchValue=[false]) {
            if (rawData == undefined) {
                return;
            }

            let data = [];
            let layout = {
                "xaxis": {"tick0": -2, "dtick": 1,
                          "type": "log", "title": {"text": "Time [s]"}, 
                          "ticks": "outside" 
                },
                "yaxis": {"title": {"text" : "G(t) [Pa]"}, "range": [0, 1.0],
                          "rangemode": "tozero", "ticks": "outside"
                },
            }
            let rawDataTrace = {
                "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
                "name": "Experiental Data",
                "mode": "markers",
                "marker": {color:"green", "symbol": "circle-open", 
                           "size": 10, "maxdisplayed": 200},
                "x": rawData.x,
                "y": rawData.y
            }

            /**
            * Only oversampling button on and oversamplingData has value to render Oversampling figure.
            * You may feel wired about the switchValue is [bool] not bool.
            * It's the Dash's wired part... Just follow the framework's rule.
            */
            if (switchValue[0] == true && oversamplingData != undefined) {
                // console.log("========= in oversampling =======");
                // console.log(oversamplingData)
                // data = oversamplingData;
                let oversamplingDataTrace = {
                    "name": "Oversampling Data",
                    "mode": "markers",
                    "marker": {color:"darkgreen", "symbol": "circle-x", 
                                "size": 6, "maxdisplayed": 200},
                    "x": oversamplingData.x,
                    "y": oversamplingData.y
                }
                
                data.push(rawDataTrace, oversamplingDataTrace);
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
            if (ftData == undefined) {
                return;
            }

            let data = [];
            let layout = {
                "xaxis": {"dtick": 1, "tick0": -12, 
                          "type": "log", "title": {"text": "ω [rad/s])"},
                          "ticks": "outside"},
                "yaxis": {"dtick": 1, "tick0": -7, 
                          "type": "log", "title": {"text" : "G′ G′′ [Pa]"},
                          "ticks": "outside"},
            }
            let ftDataTrace0 = {
                "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
                "name": "G\'",
                "mode": "markers+lines",
                // "line": {color:"black"},
                "marker": {"color": "black", "symbol": "square", "size": 7},
                "x": ftData.x,
                "y": ftData.y1,
            }
            let ftDataTrace1 = {
                "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
                "name": "G\'\'",
                "mode": "markers+lines",
                "line": {"color": "red", "symbol": "circle"},
                "x": ftData.x,
                "y": ftData.y2,
            }

            if (switchValue[0] == true && oversampledftData != undefined) {
                let oversampledftDataTrace0 = {
                    "name": "G\'",
                    "mode": "markers+lines",
                    "line": {color:"black"},
                    "marker": {"color": "black", "symbol": "square", "size": 5},
                    "x": oversampledftData.x,
                    "y": oversampledftData.y1,
                }
                let oversampledftDataTrace1 = {
                    "name": "G\'\'",
                    "mode": "markers+lines",
                    "line": {"color": "red", "symbol": "circle"},
                    "x": oversampledftData.x,
                    "y": oversampledftData.y2,
                }
                
                data.push(oversampledftDataTrace0, oversampledftDataTrace1);
            } else {
                data.push(ftDataTrace0, ftDataTrace1);  
            }

            return {
                "data" : data,
                "layout": layout
            }   
        }
    },
    clientsideGamma: {
        tabChangeFigRender: gammaRender,
    },
    clientsideMot: {
        tabChangeFigRender: motAtRender,
        tabChangeMotRender: motRender
    },
    clientsideMessageRec: {
        uploadMessage: uploadMessageRecovery
    }
});