var page_title = "DESCRIPTION";
var app = function(){
    let hostname = location.pathname.split('/')[2];
    let main_grid = document.createElement('div'), card;
    let now = moment();
    let to_datetime = now.format('YYYYMMDDHHmmss');
    let from_datetime = now.subtract('3', 'hour').format('YYYYMMDDHHmmss');
    let interval_update_target = [];

    card = new KikuCard('card_content_1', 'CPU', {});
    append(main_grid, card.createComponent(CARD_SIZE.S));
    card.setChartContentsV2(`/api/v1/os_latest/${hostname}/cpu`, CHART_TYPE.GAUGE, null);
    interval_update_target.push({"card": card, "type": "os_latest", "resource": "cpu", "chart_type": CHART_TYPE.GAUGE, "option": null});

    card = new KikuCard('card_content_2', 'MEMORY', {});
    append(main_grid, card.createComponent(CARD_SIZE.S));
    card.setChartContentsV2(`/api/v1/os_latest/${hostname}/memory`, CHART_TYPE.GAUGE, null);
    interval_update_target.push({"card": card, "type": "os_latest", "resource": "memory", "chart_type": CHART_TYPE.GAUGE, "option": null});

    card = new KikuCard('card_content_3', 'STORAGE', {});
    append(main_grid, card.createComponent(CARD_SIZE.S));
    card.setChartContentsV2(`/api/v1/os_latest/${hostname}/storage`, CHART_TYPE.GAUGE, null);
    interval_update_target.push({"card": card, "type": "os_latest", "resource": "storage", "chart_type": CHART_TYPE.GAUGE, "option": null});

    card = new KikuCard('card_content_4', 'SWAP', {});
    append(main_grid, card.createComponent(CARD_SIZE.S));
    card.setChartContentsV2(`/api/v1/os_latest/${hostname}/swap`, CHART_TYPE.GAUGE, null);
    interval_update_target.push({"card": card, "type": "os_latest", "resource": "swap", "chart_type": CHART_TYPE.GAUGE, "option": null});

    card = new KikuCard('card_content_5', 'DISK/IO', {});
    append(main_grid, card.createComponent(CARD_SIZE.S));
    card.setSimpleTextContents(`/api/v1/os_latest/${hostname}/diskio`, {'unit': ''});

    card = new KikuCard('card_content_6', 'NETWORK', {});
    append(main_grid, card.createComponent(CARD_SIZE.S));
    card.setChartContentsV2(`/api/v1/os_latest/${hostname}/network`, CHART_TYPE.GAUGE, {title: '', label: false});

    card = new KikuCard('card_content_7', 'INFOMATION', {});
    append(main_grid, card.createComponent(CARD_SIZE.M));
    card.setTableContents(`/api/v1/server/${hostname}`, null);

    card = new KikuCard('card_content_8', 'SPECIFICATION', {});
    append(main_grid, card.createComponent(CARD_SIZE.M));
    card.setTableContents(`/api/v1/server_spec/${hostname}`, null);

    card = new KikuCard('card_content_9', 'APPLICATIONS', {});
    append(main_grid, card.createComponent(CARD_SIZE.M));
    card.setTableContents(`/api/v1/server_application/${hostname}`, null);

    card = new KikuCard('card_content_10', 'CPU HISTORY', {});
    append(main_grid, card.createComponent(CARD_SIZE.L));
    card.setChartContentsV2(`/api/v1/os/${hostname}/cpu/${from_datetime}/${to_datetime}`, CHART_TYPE.ARIA_SPLINE, {"maxY": 100});
    interval_update_target.push({"card": card, "type": "os", "resource": "cpu", "chart_type": CHART_TYPE.ARIA_SPLINE, "option": {"maxY": 100}});

    card = new KikuCard('card_content_11', 'MEMORY HISTORY', {});
    append(main_grid, card.createComponent(CARD_SIZE.L));
    card.setChartContentsV2(`/api/v1/os/${hostname}/memory/${from_datetime}/${to_datetime}`, CHART_TYPE.ARIA_SPLINE, {"maxY": 100});
    interval_update_target.push({"card": card, "type": "os", "resource": "memory", "chart_type": CHART_TYPE.ARIA_SPLINE, "option": {"maxY": 100}});

    card = new KikuCard('card_content_12', 'SWAP HISTORY', {});
    append(main_grid, card.createComponent(CARD_SIZE.L));
    card.setChartContentsV2(`/api/v1/os/${hostname}/swap/${from_datetime}/${to_datetime}`, CHART_TYPE.ARIA_SPLINE, {"maxY": 100});
    interval_update_target.push({"card": card, "type": "os", "resource": "swap", "chart_type": CHART_TYPE.ARIA_SPLINE, "option": {"maxY": 100}});

    card = new KikuCard('card_content_13', 'STORAGE HISTORY', {});
    append(main_grid, card.createComponent(CARD_SIZE.L));
    card.setChartContentsV2(`/api/v1/os/${hostname}/storage/${from_datetime}/${to_datetime}`, CHART_TYPE.ARIA_SPLINE, {"maxY": 100});
    interval_update_target.push({"card": card, "type": "os", "resource": "storage", "chart_type": CHART_TYPE.ARIA_SPLINE, "option": {"maxY": 100}});

    card = new KikuCard('card_content_14', 'DISKIO HISTORY', {});
    append(main_grid, card.createComponent(CARD_SIZE.L));
    card.setChartContentsV2(`/api/v1/os/${hostname}/diskio/${from_datetime}/${to_datetime}`, CHART_TYPE.ARIA_SPLINE, {"maxY": null});
    interval_update_target.push({"card": card, "type": "os", "resource": "diskio", "chart_type": CHART_TYPE.ARIA_SPLINE, "option": {"maxY": null}});


    for(let i of interval_update_target){
        console.log(i);
    }

    setInterval(function(){
        let now = moment();
        let to_datetime = now.format('YYYYMMDDHHmmss');
        let from_datetime = now.subtract('3', 'hour').format('YYYYMMDDHHmmss');
        for(let i of interval_update_target){
            if(i["type"] == "os_latest"){
                i["card"].setChartContentsV2(`/api/v1/${i["type"]}/${hostname}/${i["resource"]}`, i["chart_type"], i["option"]);
            }

            switch (i["type"]) {
                case "os_latest":
                    i["card"].setChartContentsV2(`/api/v1/${i["type"]}/${hostname}/${i["resource"]}`, i["chart_type"], i["option"]);
                    break;
                case "os":
                    i["card"].setChartContentsV2(`/api/v1/${i["type"]}/${hostname}/${i["resource"]}/${from_datetime}/${to_datetime}`, i["chart_type"], i["option"]);
                    break;
                default:
                    break;
            }
        }
    }, 60*1000);
    setTimeout(function(){location.reload()}, 5 * 60 * 1000);

    return main_grid;
}

function append(parent, child){
    parent.insertAdjacentElement("beforeend", child);
}