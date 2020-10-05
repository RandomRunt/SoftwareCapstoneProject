//Will add my js here later
function chartGeneartor(dataInput){
    var datafull = {
        lables: dataInput[1],
        datasets: dataInput[2]
    };
    return {
        type: dataInput.type,
        data: {
            lables,
            datasets
        }

    }
}
