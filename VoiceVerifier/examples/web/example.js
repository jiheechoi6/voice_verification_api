let BASE = "http://175.197.109.183:3000/"

console.log("hello")

async function readFile(evt){
    let uuid1 = await createStream()
    let uuid2 = await createStream()
    console.log(uuid1)
    console.log(uuid2)

    let f1 = document.getElementById("fileinput").files[0];
    let f2 = document.getElementById("fileinput2").files[0];

    await sendToStream(uuid1, f1)
    await sendToStream(uuid2, f2)

    await new Promise(r => setTimeout(r, 1000));

    await enroll("test", uuid1)
    let verResult = await verify("test", uuid2)
    let result = verResult["result"]
    console.log(result)
    let score = verResult["score"]

    document.getElementById('score_card').innerText = result+"  (score: "+score.toFixed(7).toString()+")"
    let color = "green"
    if(result == "False"){
        color = "red"
    }
    document.getElementById('score_card').style.color = color
}

//###############################################################//
//######################  Helper Methods  #######################//
//###############################################################//

async function createStream(){
    let res = await fetch(BASE+"start_stream", { method: 'POST' })

    console.log(res)
    res = await res.json()

    return res['uuid']
}

async function sendToStream(uuid, f){
    if(!f){
        alert("Failed to load file");
    }

    let r = new FileReader();
    r.readAsBinaryString(f)
    r.onload = async function(e) { 
        let contents = e.target.result;
        b64content = btoa(contents)

        let res = await fetch(BASE+"upload_stream_data/"+uuid, { 
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({"data": b64content})
        })

        return b64content
    }   
}

async function enroll(external_id, uuid){
    console.log(uuid)
    await fetch(BASE+ "vv/delete_enrollment/"+external_id, {method: "DELETE"})
    let res = await fetch(BASE+"vv/enroll", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"external_id": external_id, "uuid": uuid})
    })
    console.log(res)
}

async function verify(external_id, uuid){
    let res = await fetch(BASE+"vv/verify", {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({"external_id": external_id, "uuid": uuid})
    })
    res = await res.json()
    console.log(res)
    return {"result":res["result"], "score": res["score"]}
}

document.getElementById('btn').addEventListener('click', readFile)

