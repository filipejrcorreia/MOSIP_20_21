var barbearia = {
    relogio: 0,

    barbeiros: [
        {
            estado: "livre",
            clienteEmCorte: undefined
        }, {
            estado: "livre",
            clienteEmCorte: undefined
        }, {
            estado: "livre",
            clienteEmCorte: undefined
        }
    ],
    filaEspera: [],
    criterioParagem: 100,
    numClientesAtendidos: 0,
    estado: "fechada",
    eventos: []
}


function cliente_chegada() {

    if (barbearia.estado == "aberta") {
        var barbeiroLivreIndex = getBarbeiroLivreIndex();

        if (barbeiroLivreIndex != -1 && barbearia.filaEspera == 0) {

            barbearia.barbeiros[barbeiroLivreIndex].estado = "ocupado";
            var tempoCorte = calculaTempoCorte();

            barbearia.eventos.push({ "tipo": "fim_corte", "momento": barbearia.relogio + tempoCorte, "barbeiro": barbeiroLivreIndex }); //escalonar fim_corte
        } else {
            barbearia.filaEspera += 1;
        }

        proximaChegada = barbearia.relogio + calculaTempoChegada();

        barbearia.eventos.push({ "tipo": "cliente_chegada", "momento": proximaChegada });
    }

}

function fim_corte(barbeiroIdx) {
    barbearia.barbeiros[barbeiroIdx].estado = "livre";
    barbearia.numClientesAtendidos += 1;

    if (barbearia.filaEspera > 0) {
        barbearia.filaEspera -= 1;
        barbearia.barbeiros[barbeiroIdx].estado = "ocupado";
        var tempoCorte = calculaTempoCorte();
        console.log("teste")
        barbearia.eventos.push({ "tipo": "fim_corte", "momento": barbearia.relogio + tempoCorte, "barbeiro": barbeiroIdx }); //escalonar fim_corte

    }
}



function terminarSimulacao() {
    console.log("A barbearia fechou!\n");
    console.log("Foram atendidos " + barbearia.numClientesAtendidos + " clientes!");
    console.log("log: ");
    console.log(barbearia.eventos);
}




function avancarRelogio() {

    var eventos = getNextEventos();

    if (!eventos) {
        terminarSimulacao();
        return;
    }

    //console.log(evento);

    barbearia.relogio = eventos[0].momento;

    eventos.forEach(evento => {
        
        if (evento.tipo == "fim_corte") {
            fim_corte(evento.barbeiro);
        }

        if (evento.tipo == "cliente_chegada" && barbearia.estado == "aberta") {
            cliente_chegada();
        }

        if (evento.tipo == "fecho") {
            barbearia.estado = "fechada";
        }
    });
    avancarRelogio();
}


function getNextEventos() {
    eventosPorEscalonar = barbearia.eventos.sort((a, b) => (a.momento) - (b.momento));

    eventosPorEscalonar = eventosPorEscalonar.filter(x => x.momento > barbearia.relogio);

    if (eventosPorEscalonar.length == 0) {
        return undefined;
    }

    return eventosPorEscalonar.filter(evento =>  evento.momento == eventosPorEscalonar[0].momento )
}

//###########################//
function calculaTempoChegada() {
    return getRandomNumber(1, 19);
}

function calculaTempoCorte() {
    return getRandomNumber(1, 22);
}

function getRandomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getBarbeiroLivreIndex() {
    for (let i = 0; i < barbearia.barbeiros.length; i++) {
        if (barbearia.barbeiros[i].estado == "livre") return i;
    }
    return -1;
}

function allBarbeirosLivres() {
    var ocupados = barbearia.barbeiros.find(barbeiro => barbeiro.estado == "ocupado")
    if (!ocupados) return true;
    return ocupados.length == 0;
}
//###########################//


function main() {

    //iniciar simulação
    barbearia.eventos = [];
    barbearia.barbeiros.forEach(barbeiro => {
        barbeiro.estado = "livre";
    });
    barbearia.estado = "aberta";
    barbearia.numClientesAtendidos = 0;
    barbearia.relogio = 0;
    barbearia.eventos.push({ "tipo": "fecho", momento: barbearia.criterioParagem })
    proximaChegada = calculaTempoChegada();
    barbearia.eventos.push({ "tipo": "cliente_chegada", "momento": proximaChegada });
    
    avancarRelogio();
}

main();