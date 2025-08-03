const select_box = document.getElementById('select')
const search_input = document.getElementById('search')

search_input.addEventListener('keydown', p => {
    if (p.key === 'Enter') {
        p.preventDefault()
    }
})

search_input.addEventListener('keyup', p => {
    // console.log(p)
    if (p.key === 'Enter') {
        console.log(select_box.value, search_input.value) // TODO send to rear-end
        post(search_net, {label: select_box.value, input: search_input.value}).then(response => {
            console.log(response)
            if (response.data.nodes.length === 0) {
                alert('未找到相关结果')
            } else {
                clear_data()
                knowledge_data.nodes.update(response.data.nodes)
                knowledge_data.edges.update(response.data.edges)
            }
        })
    }
})


window.onload = event => {
    get(search_init).then(data => {
        // console.log(data.data)

        clear_data()
        // for (let edge of data.data.edges) {
        //     edges_set.add(edge)
        // }
        // console.log(edges_set)
        knowledge_data.nodes.add(data.data.nodes)
        knowledge_data.edges.add(data.data.edges)
        // knowledge_data.nodes = []
        // knowledge_data.edges = []
        // console.log(knowledge_data)
        // knowledge_graph.setData(knowledge_data)

        // knowledge_data.nodes.push({id: 1522523525, label: 'fff'})
        // knowledge_graph.addNode({id: 1522523525, label: 'fff'})
        // knowledge_graph.redraw()
    })
    get(down_select).then(data => {
        // console.log(data)

        select_box.innerHTML = ''
        for (let key in data.data) {
            let node = document.createElement('option')
            if (key === 'All') node.setAttribute('selected', 'selected')
            node.setAttribute('value', key)
            node.textContent = data.data[key]
            select_box.append(node)
        }
    })
    // TODO to get values of select from rear-end
    // TODO load knowledge-graph by network request
}
