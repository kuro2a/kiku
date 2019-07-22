// Chart libraries for kiku.
const CARD_SIZE = {
    S: 1,
    M: 2,
    L: 3,
    LL: 4,
    XL: 6
};
const CHART_TYPE = {
    LINE: 1,
    GAUGE: 2,
    ARIA: 3,
    ARIA_SPLINE: 4,
    DONUT: 5,
    BAR: 6
};

/**
 * Return card size class string for UIKit.
 * 
 * @param {string} size Card size class definition value.
 */
function getCardClass(size) {
    switch (size) {
        case CARD_SIZE.XL:
            return 'uk-width-1-1@s uk-width-1-1@m uk-width-1-1@l uk-width-1-1@xl';
        case CARD_SIZE.LL:
            return 'uk-width-1-1@s uk-width-2-3@m uk-width-2-3@l uk-width-2-3@xl';
        case CARD_SIZE.L:
            return 'uk-width-1-1@s uk-width-1-2@m uk-width-1-2@l uk-width-1-2@xl';
        case CARD_SIZE.M:
            return 'uk-width-1-1@s uk-width-1-2@m uk-width-1-3@l uk-width-1-3@xl';
        case CARD_SIZE.S:
        default:
            return 'uk-width-1-2@s uk-width-1-3@m uk-width-1-6@l uk-width-1-6@xl';
    }
}

/**
 * Create table DOM. It's using classname for UIKit CSS.
 * 
 * @param {Array} header A String list.
 * @param {object} data A JSON object list. 
 */
function getTable(header, data) {
    let table, thead, tbody, tRow, tData;
    table = document.createElement("table");
    table.classList.add("uk-table", "uk-table-striped", "uk-small", "uk-table-divider", "uk-table-hover", "uk-table-middle");
    thead = document.createElement("thead");
    tbody = document.createElement("tbody");

    tRow = document.createElement("tr");
    for (let i in header) {
        tData = document.createElement("th");
        tData.innerText = header[i];
        tRow.appendChild(tData)
    }
    thead.appendChild(tRow);
    for (let i in data) {
        tRow = document.createElement("tr");
        for (let j in header) {
            tData = document.createElement("td");
            tData.innerText = data[i][header[j]];
            tRow.appendChild(tData)
        }
        tbody.appendChild(tRow);
    }
    table.appendChild(thead);
    table.appendChild(tbody);

    return table;
}


/**
 * Create simple text DOM. It's using classname for UIKit CSS.
 * 
 * @param {Array} header A String list.
 * @param {object} data A JSON object list. 
 */
function getSimpleTexts(header, data, option) {
    let top, tLabel, tValue, unit = '';
    top = document.createElement("div");

    if(option != undefined && option['unit'] != undefined){
        unit = option['unit']
    }

    for(let i of header){
        tLabel = document.createElement("div");
        tLabel.classList.add("uk-text-small", "uk-text-center");
        tLabel.innerText = `${i} ${unit}`;
        tValue = document.createElement("div");
        tValue.classList.add("uk-text-large", "uk-text-bold", "uk-text-center");
        tValue.innerText = Number(data[0][i]).toLocaleString();
        top.appendChild(tLabel);
        top.appendChild(tValue);
    }

    return top;
}

/**
 * Bind C3.js line chart to DOM in card body.
 * 
 * @param {string} id Bind DOM ID. 
 * @param {Array} data C3.js data object array. 
 * @param {string} key  C3.js data header array.
 * @return {chart} C3 chart object.
 */
function bindLineChart(id, data, key, maxY) {
    let chart = c3.generate({
        bindto: id,
        size: {
            height: 130
        },
        data: {
            x: 'timestamp',
            xFormat: '%Y/%m/%d %H:%M:%S',
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
                min: 0.0,
                max: maxY,
                padding: {
                    top: 0,
                    bottom: 0
                }
            }
        }
    });

    return chart;
}

function bindAriaChart(id, data, key, type, maxY) {
    let chart = c3.generate({
        bindto: id,
        size: {
            height: 130
        },
        data: {
            x: 'timestamp',
            xFormat: '%Y/%m/%d %H:%M:%S',
            json: data,
            keys: {
                x: 'timestamp',
                value: key
            },
            type: type
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%H:%M'
                }
            },
            y: {
                min: 0.0,
                max: maxY,
                padding: {
                    top: 0,
                    bottom: 0
                },
                tick: {
                    count: 6
                }
            }
        }
    });

    return chart;
}

function bindGaugeChart(id, data, key) {
    let chart = c3.generate({
        bindto: id,
        size: {
            height: 130
        },
        data: {
            type: 'gauge',
            json: data,
            keys: {
                value: key
            },
        },
        color: {
            pattern: ['#60B044', '#F6C600', '#F97600', '#FF0000'],
            threshold: {
                values: [50, 70, 90, 100]
            }
        }
    });

    return chart;
}

function bindDonutChart(id, data, key, title, labelFlag) {
    let chart = c3.generate({
        bindto: id,
        size: {
            height: 130
        },
        data: {
            type: 'donut',
            json: data,
            keys: {
                value: key
            }
        },
        donut: {
            title: title,
            label: {
                show: labelFlag
            }
        }
    });

    return chart;
}

function bindBarChart(id, data, key) {
    let chart = c3.generate({
        bindto: id,
        size: {
            height: 130
        },
        data: {
            type: 'bar',
            json: data,
            keys: {
                value: key
            }
        },
        bar: {
            zerobased: true
        }
    });

    return chart;
}

/**
 * Kiku card component class.
 * 
 * @constructor
 * @param {string} id Basic card IDs.
 * @param {string} title Card title.
 */
var KikuCard = function(id, title) {
    this.id = id;
    this.title = title;
    this.component = null;
    this.header = null;
    this.body = null;
    this.footer = null;
    this.contents = null;
}

/**
 * Create card component by DOM.
 * 
 * @param {CARD_SIZE} card_size Size of card component. This parameter is defined constrained variable S,M,L,LL,XL.
 * @return {element} Card component DOM.
 */
KikuCard.prototype.createComponent = function(card_size) {
    this.component = document.createElement("div");
    this.component.id = this.id;
    this.component.setAttribute("class", `uk-grid-item-match ${getCardClass(card_size)}`);
    this.body = document.createElement("div");
    this.body.classList.add("uk-card", "uk-card-default", "uk-card-hover", "uk-card-body");
    this.header = document.createElement("h3");
    this.header.classList.add("uk-card-title");
    this.header.innerText = this.title;
    this.contents = document.createElement("div");
    this.contents.id = `card_contents_${this.id}`;
    this.contents.classList.add("app-card-contents");
    let spinner = document.createElement('div');
    spinner.setAttribute("uk-spinner", "ratio: 3");
    spinner.classList.add("uk-position-center");
    this.contents.insertAdjacentElement("beforeend", spinner);

    this.body.insertAdjacentElement("beforeend", this.header);
    this.body.insertAdjacentElement("beforeend", this.contents);
    this.component.insertAdjacentElement("beforeend", this.body);

    return this.component;
}

/**
 * Clear card contents.
 */
KikuCard.prototype.clearContents = function() {
    this.contents.textContent = null;
}

/**
 * Add contents to card body.
 */
KikuCard.prototype.add = function(element) {
    this.contents.insertAdjacentElement("beforeend", element);
}

/**
 * Set chart to card body.
 * @param {string} url URL path.
 * @param {string} type Chart type.
 * @param {object} option Call method option.
 */
KikuCard.prototype.setChartContentsV2 = function(url, type, option) {
    let id = `#${this.contents.id}`,
        self = this;

    axios.get(url)
        .then(function(response) {
            meta = response['data']['meta'];
            if (meta['status'] == 'OK') {
                data = response['data']['data']['data'];
                header = response['data']['data']['key'];

                self.clearContents();
                switch (type) {
                    case CHART_TYPE.LINE:
                        bindLineChart(id, data, header, option['maxY']);
                        break;
                    case CHART_TYPE.GAUGE:
                        bindGaugeChart(id, data, header);
                        break;
                    case CHART_TYPE.ARIA:
                        bindAriaChart(id, data, header, 'aria', option['maxY']);
                        break;
                    case CHART_TYPE.ARIA_SPLINE:
                        bindAriaChart(id, data, header, 'area-spline', option['maxY']);
                        break;
                    case CHART_TYPE.DONUT:
                        bindDonutChart(id, data, header, option.title, option.label);
                        break;
                    case CHART_TYPE.BAR:
                        bindBarChart(id, data, header);
                        break;
                    default:
                        break;
                }
            }
        })
        .catch(function(error) {
            console.log(error);
        })
        .then(function() {
            // always executed
        });
}

KikuCard.prototype.setMultiChartContentsV2 = function(url, type, query, option) {
    let id = `#${this.contents.id}`,
        self = this;

    axios.post(url)
        .then(function(response) {
            meta = response['data']['meta'];
            if (meta['status'] == 'OK') {
                data = response['data']['data']['data'];
                header = response['data']['data']['key'];

                self.clearContents();
                switch (type) {
                    case CHART_TYPE.LINE:
                        bindLineChart(id, data, header, option['maxY']);
                        break;
                    case CHART_TYPE.GAUGE:
                        bindGaugeChart(id, data, header);
                        break;
                    case CHART_TYPE.ARIA:
                        bindAriaChart(id, data, header, 'aria', option['maxY']);
                        break;
                    case CHART_TYPE.ARIA_SPLINE:
                        bindAriaChart(id, data, header, 'area-spline', option['maxY']);
                        break;
                    case CHART_TYPE.DONUT:
                        bindDonutChart(id, data, header, option.title, option.label);
                        break;
                    case CHART_TYPE.BAR:
                        bindBarChart(id, data, header);
                        break;
                    default:
                        break;
                }
            }
        })
        .catch(function(error) {
            console.log(error);
        })
        .then(function() {
            // always executed
        });
}

KikuCard.prototype.setTableContents = function(url, option) {
    let id = `#${this.contents.id}`,
        self = this;

    axios.get(url)
        .then(function(response) {
            meta = response['data']['meta'];
            if (meta['status'] == 'OK') {
                data = response['data']['data']['data'];
                header = response['data']['data']['key'];
                self.clearContents();
                self.add(getTable(header, data));
            }
        })
        .catch(function(error) {
            console.log(error);
        })
        .then(function() {
            // always executed
        });
}

KikuCard.prototype.setSimpleTextContents = function(url, option) {
    let id = `#${this.contents.id}`,
        self = this;

    axios.get(url)
        .then(function(response) {
            meta = response['data']['meta'];
            if (meta['status'] == 'OK') {
                data = response['data']['data']['data'];
                header = response['data']['data']['key'];
                self.clearContents();
                self.add(getSimpleTexts(header, data, option));
            }
        })
        .catch(function(error) {
            console.log(error);
        })
        .then(function() {
            // always executed
        });
}
