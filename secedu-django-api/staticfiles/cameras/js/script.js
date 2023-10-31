/* --------------------------------------------- 
# SCRIPTS 
--------------------------------------------- */


// Data Tables - DashBoard
function now() {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}
console.log(now());
// Charts - DashBoard
function gera_cor(qtd = 1) {
    var bg_color = []
    var border_color = []
    for (let i = 0; i < qtd; i++) {
        let r = Math.random() * 255;
        let g = Math.random() * 255;
        let b = Math.random() * 255;
        bg_color.push(`rgba(${r}, ${g}, ${b}, ${0.2})`)
        border_color.push(`rgba(${r}, ${g}, ${b}, ${1})`)
    }
    //console.log([bg_color, border_color])
    return [bg_color, border_color];
}

function renderiza_media_emocoes() {
    const ctx = document.getElementById('media_dia_emocoes').getContext('2d');
    var cores_despesas_mensal = gera_cor(qtd = 12)
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            datasets: [{
                label: 'Despesas',
                data: [12, 19, 3, 5, 2, 3, 12, 19, 3, 5, 2, 3],
                backgroundColor: "#CB1EA8",
                borderColor: "#FFFFFF",
                borderWidth: 0.2
            }]
        },

    });
}

function renderiza_total_faces_por_dia(url) {
    fetch(url, {
        method: 'get',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        document.getElementById('total_faces_por_dia').innerHTML = data.total
    })
    
}

function renderiza_total_processamentos_por_dia(url) {
    
    fetch(url, {
        method: 'get',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {
        
        const ctx = document.getElementById('processamentos_por_dia').getContext('2d');
        var cores_faturamento_mensal = gera_cor(qtd = 12)
        const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                datasets: [{
                    label: data.labels,
                    data: data.data,
                    backgroundColor: cores_faturamento_mensal[0],
                    borderColor: cores_faturamento_mensal[1],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });    
    })
}
/* ---------------------------------------------



function renderiza_produtos_mais_vendidos(url) {

    fetch(url, {
        method: 'get',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {

        const ctx = document.getElementById('produtos_mais_vendidos').getContext('2d');
        var cores_produtos_mais_vendidos = gera_cor(qtd = 4)
        const myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Despesas',
                    data: data.data,
                    backgroundColor: cores_produtos_mais_vendidos[0],
                    borderColor: cores_produtos_mais_vendidos[1],
                    borderWidth: 1
                }]
            },

        });


    })

}

function renderiza_funcionario_mes(url) {



    fetch(url, {
        method: 'get',
    }).then(function (result) {
        return result.json()
    }).then(function (data) {

        const ctx = document.getElementById('funcionarios_do_mes').getContext('2d');
        var cores_funcionarios_do_mes = gera_cor(qtd = 4)
        const myChart = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: cores_funcionarios_do_mes[0],
                    borderColor: cores_funcionarios_do_mes[1],
                    borderWidth: 1
                }]
            },

        });


    })

}
*/