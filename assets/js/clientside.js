const RENDER_DATA = {
    "RAW_DATA": 0,
    "OVERSAMPLING_DATA": 1
}

const FTAPP_TIME_DERIVATED = {
    "NONTIME_DERIVATED": 0,
    "TIME_DERIVATED": 1
}

const FUNCTION_TYPE = {
    "AT"   : 0,
    "PAI_T": 1
}

/**
* oversamplingSwitchValue, true false
* timeDerivative, true false
* totally 4 status
*/
figSetting = (ftData, oversampledftData, oversamplingSwitch, timeDerivativedSwitch, verticalAxisSwitch) => {
    // if the oversampledftData is null, setting the oversamplingSwitch false even if true
    if (oversamplingSwitch == true) {
        oversamplingSwitch = oversampledftData == undefined ? false : true;
    }

    let setting = {};
    // setting xaxisText
    let xaxisText = timeDerivativedSwitch == true ?
        "Omega [rad/s]" : "Frequency [Hz]";
    
    setting["text"] = xaxisText;
    setting["yaxis"] = {"dtick": 1, "tick0": -7, 
        "type": "log", "title": {"text" : "R, I"},
        "ticks": "outside"
    };

    if (oversamplingSwitch && timeDerivativedSwitch) {
        setting["x"] = oversampledftData.x;
        setting["y1"] = oversampledftData.y1;
        setting["y2"] = oversampledftData.y2;
    } else if (oversamplingSwitch) {
        setting["x"] = oversampledftData.x;
        setting["y1"] = oversampledftData.non_time_y1;
        setting["y2"] = oversampledftData.non_time_y2;
        setting["yaxis"] = {"type": "linear", 
            "title": {"text" : "R, I"},
            "ticks": "outside"};
    } else if (timeDerivativedSwitch) {
        setting["x"] = ftData.x;
        setting["y1"] = ftData.y1;
        setting["y2"] = ftData.y2;
    } else {
        setting["x"] = ftData.x;
        setting["y1"] = ftData.non_time_y1;
        setting["y2"] = ftData.non_time_y2;
        setting["yaxis"] = {"type": "linear", 
        "title": {"text" : "R, I"},
        "ticks": "outside"};
    }

    if (verticalAxisSwitch) {
        setting["yaxis"]["type"] = "linear";
    } else {
        setting["yaxis"]["type"] = "log";
    }

    return setting;
}


// Function implementation list
gammaRender = function(rawData, oversamplingData, switchValue=[false], verticalAxisSwitch=[false]) {
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
                "type": "log",
                "rangemode": "tozero", "ticks": "outside"
        },
    };
    let rawDataTrace = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "Experiental Data",
        "mode": "markers",
        "marker": {color:"orange", "symbol": "circle-open", 
                "size": 10, "maxdisplayed": 200},
        "x": rawData.x,
        "y": rawData.z
    };

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
        };
        
        data.push(rawDataTrace, oversamplingDataTrace);
    } else {
        // console.log("========= in sigma =============");
        // console.log(rawData)
        // data = rawData;
        data.push(rawDataTrace);
    }

    if (verticalAxisSwitch[0]) {
        layout["yaxis"]["type"] = "linear"
    } else {
        layout["yaxis"]["type"] = "log"
    }
    return {
        "data" : data,
        "layout": layout
    };
}

motAtRender = function(rawData, oversamplingData, switchValue=[false], verticalAxisSwitch=[false]) {
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
                "type": "log",
                "rangemode": "tozero", "ticks": "outside"
        },
    };
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
        };

        data.push(rawDataTrace, oversamplingDataTrace);
    } else {
        // console.log("========= in sigma =============");
        // console.log(rawData)
        // data = rawData;
        data.push(rawDataTrace);
    }

    if (verticalAxisSwitch[0]) {
        layout["yaxis"]["type"] = "linear"
    } else {
        layout["yaxis"]["type"] = "log"
    }

    return {
        "data" : data,
        "layout": layout
    };
}

motRender = function(ftData, oversampledftData, switchValue=[false], 
                     functionFlag, verticalAxisSwitch = [false])  
{
    if (ftData == undefined) {
        return;
    }

    let x, y1, y2;

    if (functionFlag == FUNCTION_TYPE.AT) {
        x  = ftData.x;
        y1 = ftData.at_y1;
        y2 = ftData.at_y2;
    } else {
        x  = ftData.x;
        y1 = ftData.pai_y1;
        y2 = ftData.pai_y2;
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
    };
    let ftDataTrace0 = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "G'",
        "mode": "lines",
        "line": {color:"black"},
        "x": x,
        "y": y1,
    };
    let ftDataTrace1 = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "G''",
        "mode": "lines",
        "line": {color:"red"},
        "x": x,
        "y": y2,
    };

    if (switchValue[0] == true && oversampledftData != undefined) {
        if (functionFlag == FUNCTION_TYPE.AT) {
            x  = oversampledftData.x;
            y1 = oversampledftData.at_y1;
            y2 = oversampledftData.at_y2;
        } else {
            x  = oversampledftData.x;
            y1 = oversampledftData.pai_y1;
            y2 = oversampledftData.pai_y2;
        }
        
        let oversampledftDataTrace0 = {
            "name": "Oversampled-G'",
            "mode": "lines",
            "line": {color:"black"},
            "x": x,
            "y": y1,
        };
        let oversampledftDataTrace1 = {
            "name": "Oversampled-G''",
            "mode": "lines",
            "line": {color:"red"},
            "x": x,
            "y": y2,
        };
        
        data.push(oversampledftDataTrace0, oversampledftDataTrace1);
    } else {
        data.push(ftDataTrace0, ftDataTrace1);  
    }

    if (verticalAxisSwitch[0]) {
        layout["yaxis"]["type"] = "linear"
    } else {
        layout["yaxis"]["type"] = "log"
    }

    return {
        "data" : data,
        "layout": layout
    };
}

reImFigRender = function(ftData, oversampledftData, 
    oversamplingSwitchValue=[false], timeDerivatived=[false], verticalAxisSwitch=[false]) {
    if (ftData == undefined) {
        return;
    }

    let setting = figSetting(ftData, oversampledftData, 
        oversamplingSwitchValue[0], timeDerivatived[0], verticalAxisSwitch[0])
    
    let data = [];
    let layout = {
        "xaxis": {"dtick": 1, "tick0": -12, 
                  "type": "log", "title": {"text": setting.text},
                  "ticks": "outside"},
        "yaxis": setting.yaxis
    };
    let ftDataTrace0 = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "real",
        "mode": "lines",
        "line": {color:"black"},
        "x": setting.x,
        "y": setting.y1,
    };
    let ftDataTrace1 = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "imaginary",
        "mode": "lines",
        "line": {color:"red"},
        "x": setting.x,
        "y": setting.y2,
    };

    if (oversamplingSwitchValue[0] == true && oversampledftData != undefined) {
        let oversampledftDataTrace0 = {
            "name": "Oversampled-real",
            "mode": "lines",
            "line": {color:"black"},
            "x": setting.x,
            "y": setting.y1,
        };
        let oversampledftDataTrace1 = {
            "name": "Oversampled-imaginary",
            "mode": "lines",
            "line": {color:"red"},
            "x": setting.x,
            "y": setting.y2,
        };
        
        data.push(oversampledftDataTrace0, oversampledftDataTrace1);
    } else {
        data.push(ftDataTrace0, ftDataTrace1);  
    }

    return {
        "data" : data,
        "layout": layout
    };
}

forceRender = function(rawData) {
    if (rawData == undefined) {
        return;
    }

    let data = [];
    let layout = {
        "xaxis": {"dtick": 1, "tick0": -12, 
                  "type": "log", "title": {"text": "Time (s)"},
                  "ticks": "outside"},
        "yaxis": {"dtick": 1, "tick0": -7, 
                  "type": "log", "title": {"text" : "Force (uN)"},
                  "ticks": "outside"},
    };

    let rawDataTrace = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "force-time",
        "mode": "markers",
        "marker": {"symbol": "circle-open", 
                "size": 10, "maxdisplayed": 200},
        "x": rawData.x,
        "y": rawData.y
    }

        data.push(rawDataTrace);

    return {
        "data" : data,
        "layout": layout
    };
}

identationRender = function(rawData) {
    if (rawData == undefined) {
        return;
    }

    let data = [];
    let layout = {
        "xaxis": {"dtick": 1, "tick0": -12, 
                  "type": "log", "title": {"text": "Time (s)"},
                  "ticks": "outside"},
        "yaxis": {"dtick": 1, "tick0": -7, 
                  "type": "log", "title": {"text" : "Force (uN)"},
                  "ticks": "outside"},
    };

    let rawDataTrace = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "Identation-time",
        "mode": "markers",
        "marker": {"symbol": "circle-open", 
                "size": 10, "maxdisplayed": 200},
        "x": rawData.x,
        "y": rawData.z
    }

        data.push(rawDataTrace);

    return {
        "data" : data,
        "layout": layout
    };
}

afmRender = function(ftData, oversampledData, switchValue=[false], verticalAxisSwitch=[false]) {
    if (ftData == undefined) {
        return;
    }

    let data = [];
    let layout = {
        "xaxis": {"tick0": -2, "dtick": 1,
                "type": "log", 
                "title": {"text": "t (sec)"}, 
                "ticks": "outside" 
        },
        "yaxis": {"title": {"text" : "A(t)"},
                "type": "log",
                "rangemode": "tozero", "ticks": "outside"
        },
    };
    let ftDataTrace1 = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "Experiental Data",
        "mode": "markers",
        "marker": {"symbol": "circle-open", 
                "size": 10, "maxdisplayed": 200},
        "x": ftData.x,
        "y": ftData.y1
    }
    let ftDataTrace2 = {
        "hovertemplate": "x=%{x}<br>y=%{y}<extra></extra>", 
        "name": "Experiental Data",
        "mode": "markers",
        "marker": {"symbol": "circle-open", 
                "size": 10, "maxdisplayed": 200},
        "x": ftData.x,
        "y": ftData.y2
    }

    if (switchValue[0] == true && oversampledData != undefined) {
        let oversampledDataTrace1 = {
            "name": "Oversampling Data",
            "mode": "markers",
            "marker": {"symbol": "circle-x", 
                        "size": 6, "maxdisplayed": 200},
            "x": oversampledData.x,
            "y": oversampledData.y1
        };
        let oversampledDataTrace2 = {
            "name": "Oversampling Data",
            "mode": "markers",
            "marker": {"symbol": "circle-x", 
                        "size": 6, "maxdisplayed": 200},
            "x": oversampledData.x,
            "y": oversampledData.y2
        };

        if (verticalAxisSwitch[0]) {
            layout["yaxis"]["type"] = "linear"
        } else {
            layout["yaxis"]["type"] = "log"
        }

        data.push(oversampledDataTrace1, oversampledDataTrace2);
    } else {
        // console.log("========= in sigma =============");
        // console.log(rawData)
        // data = rawData;
        data.push(ftDataTrace1, ftDataTrace2);
    }

    return {
        "data" : data,
        "layout": layout
    };
}

uploadMessageRecovery = function(rawData) {
    if (rawData == undefined) {
        return;
    }

    const filename = rawData.filename;
    const len = rawData.lines;

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
                "yaxis": {"title": {"text" : "Input"}, "range": [0, 1.0],
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
        tabChangeFigRender: function(ftData, oversampledftData, switchValue=[false], verticalAxisSwitch=[false]) {
            if (ftData == undefined) {
                return;
            }

            let data = [];
            let layoutLinear = {
                "xaxis": {"dtick": 1, "tick0": -12, 
                          "type": "log", "title": {"text": "ω [rad/s]"},
                          "ticks": "outside"},
                "yaxis": {"dtick": 1, "tick0": -7, 
                          "type": "linear", "title": {"text" : "G′ G′′ [Pa]"},
                          "ticks": "outside"},
            }
            let layoutLog = {
                "xaxis": {"dtick": 1, "tick0": -12, 
                          "type": "log", "title": {"text": "ω [rad/s]"},
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
            
            let layout = [];
            if (verticalAxisSwitch[0]) {
                layout = layoutlinear;
            } else {
                layout = layoutlog;
            }
            return {
                "data" : data,
                "layout": layout
            }   
        },
        tabChangeFTfigRender: reImFigRender
    },
    clientsideGamma: {
        tabChangeFigRender: gammaRender,
    },
    clientsideMot: {
        tabChangeFigRender: motAtRender,
        tabChangeMotRender: motRender
    },
    clientsideAfm: {
        tabChangeForRender: forceRender,
        tabChangeIdeRender: identationRender,
        tabChangeFunRender: afmRender,
    },
    clientsideMessageRec: {
        uploadMessage: uploadMessageRecovery
    }
});