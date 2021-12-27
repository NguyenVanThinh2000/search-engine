import logo from './2.png';

import "./Search.css";
import axios from "axios";
import React, { useState } from "react";

export default function Search() {

    var [data, setData] = useState('cranfield');
    var [tool, setTool] = useState('VSM');

    function handleResults(results, num_res, time){
        var el = document.getElementById('results');
        var e_time = document.getElementById('time');
        var para = document.createElement('p');
        para.innerText = 'About ' + num_res + ' results (' + time + ' seconds)';
        e_time.appendChild(para)
        for(let i = 0; i < results[0].length; i++){
            var child = document.createElement("div")
            var head = document.createElement('h3')
            var content = document.createElement('p')

            head.innerText = '#' + results[0][i]
            content.innerText = results[1][i]

            child.appendChild(head)
            if (results[1][i]){
                child.appendChild(content)
            }
            el.appendChild(child)
        }
    }
    function removeResults(){
        var el = document.getElementById('results');
        el.innerHTML = '';
        var e_time = document.getElementById('time');
        e_time.innerHTML = '';
    }


    function handleOnchanheData(event){
        var temp = event.target.value;
        setData(temp)
    }
    function handleOnchanheTool(event){
        var t = event.target.value;
        setTool(t)
    }
    
    function addDotsLoading(){
        var el = document.getElementById('loading');
        el.classList.remove('hide-dots-loading');
        el.classList.add('dots-loading');
    }
    function removeDotsLoading(){
        var el = document.getElementById('loading');
        el.classList.add('hide-dots-loading');
        el.classList.remove('dots-loading');
    }
    function handleSubmit(){
        var element = document.getElementById('box_input');
        var query = element.value;

        var bodyFormData = new FormData();
        bodyFormData.append("query", query);
        bodyFormData.append("data", data);
        bodyFormData.append("tool", tool);

        removeResults();
        addDotsLoading();
        axios({
            method: "post",
            url: "http://127.0.0.1:5000/search",
            data: bodyFormData,
        })
            .then(function (response) {
                var res = response["data"];
                console.log(res)
                var results = res['resuslt'];
                var num_res = res['num_res'];
                var time = res['time'];
                console.log(num_res);
                removeDotsLoading();
                handleResults(results, num_res, time);
            })
            .catch(function (error) {
                console.log(error);
            });

    }

    return(
        <div className='all'>
            <div className="input_search" id="input_search">
                <div id="big_logo" className="big_logo">
                    <img src={logo} alt="logo"/>
                </div>
                <div className="form_input">
                    <input id="box_input" className="input_box input_box_change" type="text" name="name" />
                    <button onClick={handleSubmit} id="btn_search" className="btn_search btn_search_change">
                        <ion-icon name="search"></ion-icon>
                    </button>
                </div>


                <div className="form_checkbox">
                    <div className="data">
                        <form>
                            <label>
                                cranfield 
                                <input value="cranfield" onChange={handleOnchanheData} className="cranfield"  type="radio" name="ratio"/>
                            </label>
                            <label>
                                corpus 
                                <input value="corpus" onChange={handleOnchanheData} className="corpus" type="radio" name="ratio"/>
                            </label>
                        </form>
                    </div>
                    
                    <div className="tool">
                        <form>
                            <label>
                                VSM 
                                <input value="VSM" onChange={handleOnchanheTool} className="VSM"  type="radio" name="radio"/>
                            </label>
                            <label>
                                BIM 
                                <input value="BIM" onChange={handleOnchanheTool} className="BIM" type="radio" name="radio"/>
                            </label>
                        </form>
                    </div>

                </div>
            </div>

            <div id='time' className='time'>
            </div>
            <div className="results" id="results">
            </div>
            <div id='loading' class="hide-dots-loading">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
        </div>
    )
}