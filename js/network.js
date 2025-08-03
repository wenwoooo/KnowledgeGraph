const instance = axios.create({
    baseURL: 'http://127.0.0.1:8080',
    timeout: 0,
    // withCredentials: true,
    crossDomain: true,
    headers: {
        'content-type': 'application/x-www-form-urlencoded'
    }
});

function post(url, data = null) {
    return instance.post(url, data)
}

function get(url) {
    return instance.get(url)
}

const chat_bot_init = '/robot-init'
const chat_bot_question = '/robot'

const search_init = '/init'
const search_net = '/search'
const down_select = '/down-select'
const get_node_info = '/get-node-info'
const double_click_node = '/double-click-node'
const single_click_node = '/single-click-node'
