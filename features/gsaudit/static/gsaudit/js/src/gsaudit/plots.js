
gsaudit.plots = {}

gsaudit.plots.distribution = function(target_id, series) {
    // Can specify a custom tick Array.
    // Ticks should match up one for each y value (category) in the series.
    var ticks = ['--', '-', 'o', '+', '++'];
     
    var plot1 = $.jqplot(target_id, [series], {
        // The "seriesDefaults" option is an options object that will
        // be applied to all series in the chart.
        seriesDefaults:{
            renderer:$.jqplot.BarRenderer,
            rendererOptions: {fillToZero: false, varyBarColor:true}
        },
        // Custom labels for the series are specified with the "label"
        // option on the series option.  Here a series option object
        // is specified for each series.
        series:[
            /*{label:'Hotel'},
            {label:'Event Regristration'},
            {label:'Airfare'}*/
        ],
        seriesColors: [ "#BB0014", "#BB0014", "#ddd", '#1e9817', '#1e9817'],
        // Show the legend and put it outside the grid, but inside the
        // plot container, shrinking the grid to accomodate the legend.
        // A value of "outside" would not shrink the grid and allow
        // the legend to overflow the container.
        legend: {
            //show: true,
            //placement: 'outsideGrid'
        },
        axes: {
            // Use a category axis on the x axis and use our custom ticks.
            xaxis: {
                renderer: $.jqplot.CategoryAxisRenderer,
                ticks: ticks
            },
            // Pad the y axis just a little so bars can get close to, but
            // not touch, the grid boundaries.  1.2 is the default padding.
            yaxis: {
                tickInterval: 1,
                tickOptions: {
                    formatString: '%d'
                } 
                /*pad: 1.05,
                tickOptions: {formatString: '%d'}*/
            }
        }
    })
}


gsaudit.plots.skill_development = function(target_id, series) {
    var ticks = [[-2.8, ''], [-2, '--'], [-1,'-'], [0,'o'], [1, '+'], [2, '++'], [2.8, '']];
    var xticks = []
    for (var i=0; i<=series.length + 1;i++) {
        xticks.push([i, ''+i])
    }
    var plot1 = $.jqplot (target_id, [series], {
        series: [{
            lineWidth:1, 
            markerOptions: { style:'filledCircle', color:'#999' }
        }],
        axes: {
            // Use a category axis on the x axis and use our custom ticks.
            xaxis: {
            //    renderer: $.jqplot.CategoryAxisRenderer,
                ticks: xticks,
                formatString: '%d',
                tickInterval: 1,
                 borderWidth:0,
                 pad:1.2
            },
            // Pad the y axis just a little so bars can get close to, but
            // not touch, the grid boundaries.  1.2 is the default padding.
            yaxis: {
                ticks:ticks,
                tickInterval: 1,
                borderWidth:0
                //tickOptions: {
                //formatString: '%d'
                //} 
                /*pad: 1.05,
                tickOptions: {formatString: '%d'}*/
            },
            x2axis: {borderWidth:0},
            y2axis: {borderWidth:0}
        }
    })
}
