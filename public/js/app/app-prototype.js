var app = function () {
    // If you need some original logic, write your programs are here.
    var chart = c3.generate({
        bindto: '#sample_chart_1',
        data: {
            columns: [
                ['data1', 30, 200, 100, 400, 150, 250],
                ['data2', 50, 20, 10, 40, 15, 25]
            ]
        }
    });
    getLineChart(
        '#sample_chart_1', [
            { name: 'www.site1.com', upload: 200, download: 200, total: 400 },
            { name: 'www.site2.com', upload: 100, download: 300, total: 400 },
            { name: 'www.site3.com', upload: 300, download: 200, total: 500 },
            { name: 'www.site4.com', upload: 400, download: 100, total: 500 },
        ], ['upload', 'download']
    );
    var chart = c3.generate({
        bindto: '#sample_chart_2',
        data: {
            columns: [
                ['data1', 30],
                ['data2', 120],
            ],
            type: 'donut',
            onclick: function (d, i) { console.log("onclick", d, i); },
            onmouseover: function (d, i) { console.log("onmouseover", d, i); },
            onmouseout: function (d, i) { console.log("onmouseout", d, i); }
        },
        donut: {
            title: "test"
        }
    });
    getSingleMachineResourceTimelineChart(
        '#sample_chart_3', [
            { timestamp: '2019-04-01 12:00', cpu: 40, memory: 20, storage: 5 },
            { timestamp: '2019-04-01 12:01', cpu: 80, memory: 22, storage: 5 },
            { timestamp: '2019-04-01 12:02', cpu: 20, memory: 22, storage: 5 },
            { timestamp: '2019-04-01 12:03', cpu: 77, memory: 23, storage: 5 },
            { timestamp: '2019-04-01 12:04', cpu: 10, memory: 22, storage: 5 },
            { timestamp: '2019-04-01 12:05', cpu: 23, memory: 22, storage: 5 }
        ], ['cpu', 'memory', 'storage']
    );


    getWebAccessChart(
        '#sample_chart_4', [
            { name: '/login', today: 200, "a week ago": 200 },
            { name: '/logout', today: 100, "a week ago": 300 },
            { name: '/index', today: 300, "a week ago": 200 },
            { name: '/prototype', today: 400, "a week ago": 200 },
            { name: '/page1', today: 40, "a week ago": 20 },
            { name: '/foo', today: 120, "a week ago": 200 },
            { name: '/baa', today: 150, "a week ago": 400 },
            { name: '/hoge', today: 290, "a week ago": 250 },
            { name: '/moge', today: 400, "a week ago": 30 },
            { name: '/fuga', today: 700, "a week ago": 300 },
            { name: '/version', today: 20, "a week ago": 70 },
            { name: '/help', today: 110, "a week ago": 900 },
            { name: '/datasource', today: 50, "a week ago": 2030 },
            { name: '/grab', today: 100, "a week ago": 80 },
            { name: '/facade', today: 990, "a week ago": 20 },
            { name: '/inbox', today: 1020, "a week ago": 490 },
            { name: '/sendmail', today: 2090, "a week ago": 600 },
            { name: '/pull', today: 100, "a week ago": 800 }
        ]
    );
    
    return document.createElement("div");
}


function getLineChart(id, data, key) {
    var chart = c3.generate({
        bindto: id,
        size: {
            height: 250
        },
        data: {
            json: data,
            keys: {
                x: 'name',
                value: key,
            }
        },
        axis: {
            x: {
                type: 'category'
            }
        }
    });

    return null;
}

function getSingleMachineResourceTimelineChart(id, data, key) {
    var chart = c3.generate({
        bindto: id,
        data: {
            x: 'timestamp',
            xFormat: '%Y-%m-%d %H:%M',
            json: data,
            keys: {
                x: 'timestamp',
                value: key
            }
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%H:%M'
                }
            },
            y: {
                min: 0,
                max: 100,
                padding: {
                    top: 0,
                    bottom: 0
                }
            }
        }
    });

    return chart;
}

function getWebAccessChart(id, data) {
    var chart = c3.generate({
        bindto: id,
        data: {
            json: data,
            keys: {
                x: 'name',
                value: ['today', 'a week ago']
            },
            types: {
                'today': 'bar',
                'a week ago': 'bar',
            }
        },
        axis: {
            x: {
                type: 'category'
            },
            y: {
                padding: {
                    top: 0,
                    bottom: 0
                }
            },
            rotated: true
        }
    });

    return chart;
}


function getCpuChart(id, data) {
    var chart = c3.generate({
        bindto: id,
        data: {
            json: data,
            keys: {
                x: 'name',
                value: ['today', 'a week ago']
            },
            types: {
                'today': 'bar',
                'a week ago': 'bar',
            }
        },
        axis: {
            x: {
                type: 'category'
            },
            y: {
                padding: {
                    top: 0,
                    bottom: 0
                }
            },
            rotated: true
        }
    });

    return chart;
}

// CPU chart.
function getCpuChartComponent(id, title) {
    let root, component, header, chart;

    root = document.createElement("div");
    root.id = id;
    root.setAttribute("class", "uk-grid-item-match");
    component = document.createElement("div");
    component.setAttribute("class", "uk-card uk-card-default uk-card-hover uk-card-body");
    header = document.createElement("div");
    header.innerText = title;
    chart = document.createElement("div");
    chart.id = "chart_" + id;
    chart.setAttribute("class", "app-cpu-chart");
    component.insertAdjacentElement("beforeend", header);
    component.insertAdjacentElement("beforeend", chart);
    root.insertAdjacentElement("beforeend", component);

    return root;
}

function drawCpuChartComponent(id, data) {
    c3.generate({
        bindto: "#chart_" + id,
        data: {
            x: 'timestamp',
            xFormat: '%Y-%m-%d %H:%M',
            json: data,
            keys: {
                x: 'timestamp',
                value: ['user', 'system', 'idle']
            }
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%H:%M'
                }
            },
            y: {
                min: 0,
                max: 100,
                padding: {
                    top: 0,
                    bottom: 0
                }
            }
        }
    });
}
