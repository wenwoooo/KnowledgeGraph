const send_message = document.getElementById("chat-middle-item");
const domBtm = document.getElementById("button");

const message = document.getElementById("chat-context-item");
const extra_content = document.getElementById('extra-content')
const enter = new Event('keyup')

function getNowDatetime() {
    let date = new Date();
    let year = date.getFullYear()
    let month = date.getMonth() + 1
    let day = date.getDate()
    let hour = date.getHours();
    let mm = date.getMinutes();
    return `${year}年${month}月${day}日 ${hour < 10 ? '0' + hour : hour}:${mm < 10 ? '0' + mm : mm}`
}

function addChat(content, className) {
    let oLi = document.createElement("div");
    oLi.setAttribute("class", className);
    oLi.innerHTML = content;

    console.log(send_message)

    send_message.append(oLi)
}


function createContent(content, head, direction, extra = '') {
    return `
        <div class="chat-${direction}-item-1 clearfix">${head}</div>
        <div class="chat-${direction}-item-2 clearfix">
            <div class="chat-${direction}-time clearfix">${getNowDatetime()}</div>
            <div class="chat-${direction}-content clearfix ${extra}">${content}</div>
        </div>
    `
}

function sendMessage(content) {
    extra_content.textContent = '思考中...'
    extra_content.className = 'success'

    post(chat_bot_question, {question: message.value}).then((response) => {
        extra_content.textContent = ''
        addChat(createContent(response.data, 'Ai', 'left'), 'chat-left clearfix')
        console.log(response)
    }).catch(() => {
        extra_content.textContent = '服务器错误'
        extra_content.className = 'error'

        addChat(createContent('出现错误了', 'Ai', 'left', 'error'), 'chat-left clearfix')
    })
}


domBtm.addEventListener("click", () => {
    sendMessage(message.value)
    addChat(createContent(message.value, '问', 'right'), "chat-right clearfix")
    message.value = "";
});

message.addEventListener('keydown', p => {
    if (p.key === 'Enter') {
        p.preventDefault()
    }
})
message.addEventListener('keyup', p => {
    if (p.key === 'Enter') {
        p.preventDefault()
        domBtm.dispatchEvent(enter)
    }
})

function init() {
    // TODO in testing
    domBtm.style.setProperty('pointer-events', 'none')
    send_message.innerHTML = ''
    get(chat_bot_init).then((response) => {
        console.log(response)
        domBtm.style.setProperty('pointer-events', 'auto')
        domBtm.style.removeProperty('background-color')

        extra_content.textContent = ''

        addChat(createContent(response.data, 'Ai', 'left'), 'chat-left clearfix')
        console.log(response.data);
        console.log(response.status);
        console.log(response.statusText);
        console.log(response.headers);
        console.log(response.config);
    }).catch(() => {
        extra_content.textContent = '初始化失败'
        extra_content.className = 'error'

        console.log("初始化失败")
        domBtm.style.setProperty('background-color', 'darkgrey')
    })
}

window.onload = event => {
    init()
}
