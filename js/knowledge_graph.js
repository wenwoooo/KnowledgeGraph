const options = {
    // height: '100%',
    // width: '100%',
    interaction: {
        // dragView: false,
        hover: true,
        hoverConnectedEdges: true
    },
    nodes: {
        // scaling: {label: {max: 180, maxVisible: 180}},
        shape: 'circle',
        size: 25,
        // widthConstraint: 25,
        // heightConstraint: 25,
        borderWidth: 2,
        borderWidthSelected: 5,
        chosen: true,
        // widthConstraint: 15,
        color: {
            border: '#569480',
            background: '#198754',
            highlight: {
                border: '#cfecff',
                background: '#198754'
            },
            hover: {
                border: '#cfecff',
                background: '#198754'
            }
        },
        font: {
            color: '#FFFFFF',
        }
    },
    edges: {
        arrows: {
            to: {
                enabled: true,
                scaleFactor: 0.7,
                type: "arrow"
            }
        },
        color: {
            //#263238
            color: '#a5abb6',
            highlight: '#a5abb6',
            hover: '#a5abb6',
            // inherit: 'to',
            opacity: 0.8
        },
        width: 2
    }
};

const canvas = document.getElementById('canvas');

// const set_data = {
//     nodes: new Set(),
//     edges: new Set()
// }
// const edges_set = new Set()
const knowledge_data = {
    nodes: new vis.DataSet([
        {id: 1, label: 'Node 1'},
        {id: 2, label: 'Node 2'},
        {id: 3, label: 'Node 3'},
        {id: 4, label: 'Node 4'},
        {id: 5, label: 'Node 5'}
    ]),
    edges: new vis.DataSet([
        {from: 1, to: 3, label: '属于'},
        {from: 1, to: 2, label: '属于'},
        {from: 2, to: 4, label: '属于'},
        {from: 2, to: 5, label: '属于'},
        {from: 2, to: 3, label: '属于'}
    ])
};

function clear_data() {
    // edges_set.clear()
    knowledge_data.edges.clear()
    knowledge_data.nodes.clear()
}

const knowledge_graph = new vis.Network(canvas, knowledge_data, options);
const prompt_window = document.getElementById('prompt-window')
knowledge_graph.on('doubleClick', properties => {
    console.log(properties) // TODO to complete double-click event. Loading the data of the double-click node from database.

    console.log(properties['nodes'])
    post(`${double_click_node}/${properties['nodes'][0]}`).then(response => {
        clear_data()
        knowledge_data.nodes.update(response.data.nodes)
        knowledge_data.edges.update(response.data.edges)
    })
})
knowledge_graph.on('hoverNode', properties => {
    // console.log(properties)
    post(`${get_node_info}/${properties.node}`).then(data => {
        prompt_window.innerHTML = ''
        let ul = document.createElement('ul')
        for (let key in data.data) {
            let li = document.createElement('li')
            li.textContent = `${key}: ${data.data[key]}`
            ul.append(li)
        }
        prompt_window.append(ul)
    })

    prompt_window.style.display = 'block'
    prompt_window.style.left = `${properties['event'].clientX}px`
    prompt_window.style.top = `${properties['event'].clientY}px`
})
knowledge_graph.on('blurNode', properties => {
    prompt_window.style.display = 'none'
})
knowledge_graph.on('selectNode', properties => {
    console.log(properties, properties.nodes[0]) // TODO unload the edges of selected node
    post(`${single_click_node}/${properties.nodes[0]}`).then(response => {
        // console.log('edges_set', response.data)
        knowledge_data.nodes.update(response.data.nodes)
        knowledge_data.edges.update(response.data.edges)
        // for (let item in response.data.nodes)
        //     if (!knowledge_data.nodes.includes(item))
        //         knowledge_data.nodes.push(item)
        // for (let value of response.data.edges) {
        //     // console.log(edges_set.has(value), value)
        //     if (!edges_set.has(value)) {
        //         edges_set.add(value)
        //         knowledge_data.edges.update(value)
        //     }
        // }
        // knowledge_graph.
    })
})
