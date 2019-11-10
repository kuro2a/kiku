var page_title = "DASH_BOARD";
var app = function() {
    var main_grid = document.createElement('div'),
        card;
    let now = moment();
    let to_datetime = now.format('YYYYMMDDHHmmss');
    let from_datetime = now.subtract('3', 'hour').format('YYYYMMDDHHmmss');
    let interval_update_target = [];

    card = new KikuCard('card_content_1', 'NEWS', {});
    append(main_grid, card.createComponent(CARD_SIZE.LL));

    card = new KikuCard('card_content_2', 'USERS', {});
    append(main_grid, card.createComponent(CARD_SIZE.S));
    card.setSimpleTextContents(`/api/v1/kiku/service_status/registered_user`, {'unit': '', 'label': false, 'heading_size': HEADING_SIZE.LARGE});

    card = new KikuCard('card_content_3', 'NODES', {});
    append(main_grid, card.createComponent(CARD_SIZE.S));
    card.setSimpleTextContents(`/api/v1/kiku/service_status/registered_server`, {'unit': '', 'label': false, 'heading_size': HEADING_SIZE.LARGE});

    let cpu_hist_card = new KikuCard('card_content_10', 'CPU HISTORY', {});
    append(main_grid, cpu_hist_card.createComponent(CARD_SIZE.M));

    let mem_hist_card = new KikuCard('card_content_11', 'MEMORY HISTORY', {});
    append(main_grid, mem_hist_card.createComponent(CARD_SIZE.M));

    axios.get('/api/v1/master/server')
        .then(function(response) {
            meta = response['data']['meta'];
            if (meta['status'] == 'OK') {
                data = response['data']['data']['data'];
                servers = []
                for (e of data) {
                    servers.push(e['hostname']);
                }
                cpu_hist_card.setChartContentsV2(`/api/v1/os_multiple/cpu/${from_datetime}/${to_datetime}?hostnames=${servers.join(',')}`, CHART_TYPE.ARIA_SPLINE, { "maxY": 100 });
                interval_update_target.push({ "card": cpu_hist_card, "type": "os_multiple", "resource": "cpu", "hosts": servers.join(','), "chart_type": CHART_TYPE.ARIA_SPLINE, "option": { "maxY": 100 } });
                mem_hist_card.setChartContentsV2(`/api/v1/os_multiple/memory/${from_datetime}/${to_datetime}?hostnames=${servers.join(',')}`, CHART_TYPE.ARIA_SPLINE, { "maxY": 100 });
                interval_update_target.push({ "card": mem_hist_card, "type": "os_multiple", "resource": "memory", "hosts": servers.join(','), "chart_type": CHART_TYPE.ARIA_SPLINE, "option": { "maxY": 100 } });
            }
        })
        .catch(function(error) {
            console.log(error);
        })
        .then(function() {
            // always executed
        });

    setInterval(function() {
        let now = moment();
        let to_datetime = now.format('YYYYMMDDHHmmss');
        let from_datetime = now.subtract('3', 'hour').format('YYYYMMDDHHmmss');
        for (let i of interval_update_target) {
            switch (i["type"]) {
                case "os_multiple":
                    i["card"].setChartContentsV2(`/api/v1/${i["type"]}/${i["resource"]}/${from_datetime}/${to_datetime}?hostnames=${i["hosts"]}`, i["chart_type"], i["option"]);
                    break;
                default:
                    break;
            }
        }
    }, 60 * 1000);
    setTimeout(function() { location.reload() }, 20 * 60 * 1000);

    return main_grid;
}

function append(parent, child) {
    parent.insertAdjacentElement("beforeend", child);
}