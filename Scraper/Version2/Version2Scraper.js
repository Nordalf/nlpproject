const request = require('request');
const async = require('async');
const fs = require('fs');
const $ = require('cheerio');
const base_url = 'https://version2.dk';
const news_url = 'https://version2.dk/it-nyheder';
var currentPage = 0;

var version2Urls = [];

var lastPage = 0;


request(news_url + "?page=0", (err, res, html) => {
    if(err) { 
        return console.log(err); 
    }
    lastPage = $('li.pager-item.last > a', html)[0].attribs.href.split("=")[1];
    async.whilst(
        function conditionChecker(callbackFunction) {
            callbackFunction(null, currentPage <= lastPage);
        }, 
        function makeRequestAndGetArticles(next) {
            console.log(news_url + "?page=" + currentPage);
            request(news_url + "?page=" + currentPage, (err, res, html) => {
                console.log("Callback");
                if(err) { 
                    return console.log(err); 
                }
                
                for(let i = 0; i < $('section > section > h2 > a', html).length; i++) {
                    version2Urls.push($('section > section > h2 > a', html)[i].attribs.href);
                }
                
                for(let i = 0; i < version2Urls.length; i++) {
                    if(!version2Urls[i].includes('https')) {    
                        request(base_url + version2Urls[i], (err, res, html) => {
                            if(err) {
                                return console.log(err);
                            }
                            if($("*[itemprop = 'articleBody']", html) != undefined) {
                                var domElement = $("*[itemprop = 'articleBody']", html).get(0);
                                if(domElement != undefined) {
                                    for(let j = 0; j < domElement.children.length; j++) {
                                        // console.log(domElement.children[j]);
                                        if(domElement.children[j].children != undefined) {
                                            // Fjerner annoncer og andre ligegyldige informationer
                                            // console.log(domElement.children[j].children);
                                            for(let k = 0; k < domElement.children[j].children.length; k++) {
                                                // if(domElement.children[j].children[0] != undefined) {
                                                
                                                if(domElement.children[j].children[k].data != undefined) {
                                                    fs.appendFileSync("body.txt", domElement.children[j].children[k].data);
                                                }
                                                else if(domElement.children[j].children[k].attribs != undefined) {
                                                    fs.appendFileSync("body.txt", domElement.children[j].children[k].attribs.title);
                                                }
                                                else {
                                                    console.log("Ingenting her");
                                                }
                                                // }
                                            }
                                            
                                            
                                            // if(domElement.children[j].children.length > 1) {
                                            //     for(let k = 1; k < domElement.children[j].children.length; k++) {
                                            //         // Her findes der tekst fra hyperlinks
                                            //         if(domElement.children[j].children[k].children != undefined && domElement.children[j].children[k].children[0] != undefined) {
                                            //             fs.appendFile("body.txt", domElement.children[j].children[k].children[0].data + ". ", (err) => {
                                            //                 if(err){
                                            //                     console.log(err);
                                            //                 }
                                            //             }); 
                                            //         }
                                            //     }
                                            // }
                                        }
                                        
                                    }
                                }
                            } else {
                                console.log("Det er en blog!");
                            }
                        });
                    }
                }
                
                version2Urls = [];
                currentPage++;
                setTimeout(() => {
                    next(null,currentPage);
                }, 1000);
            });
        }, 
        function(err, n) {
            console.log("Everything went fine: " + n );
            
        });
});



    // .then(function(html) {
    //     for(let i = 0; i < $('section > section > h2 > a', html).length; i++) {
    //         version2Urls.push($('section > section > h2 > a', html)[i].attribs.href);
    //     }
        
    //     if($('li.pager-item.is-disable.next', html)) {
    //         next = false;
    //         console.log($('li.pager-item.is-disable.next', html));
    //         break;
    //     }
        
    //     return version2Urls;
    // })
    // .then(function(input_array) {
    //     for(let i = 0; i < input_array.length; i++) {
    //         if(!input_array[i].includes('https')) {    
    //             rp(base_url + input_array[i])
    //             .then(function(html) {
    //                 if($("*[itemprop = 'articleBody']", html) != undefined) {
    //                     var domElement = $("*[itemprop = 'articleBody']", html).get(0);
    //                     if(domElement != undefined) {
    //                         for(let j = 0; j < domElement.children.length; j++) {
                                
    //                             if(domElement.children[j].children != undefined) {
    //                                 // Fjerner annoncer og andre ligegyldige informationer
    //                                 if(domElement.children[j].children[0] != undefined) {
    //                                     // body += domElement.children[j].children[0].data + ". ";
    //                                     fs.appendFile("body.txt", domElement.children[j].children[0].data + ". ", (err) => {
    //                                         if(err){
    //                                             console.log(err);
    //                                         }
    //                                     }); 
    //                                 }
        
    //                                 if(domElement.children[j].children.length > 1) {
    //                                     for(let k = 1; k < domElement.children[j].children.length; k++) {
    //                                         // Her findes der tekst fra hyperlinks
    //                                         if(domElement.children[j].children[k].children != undefined && domElement.children[j].children[k].children[0] != undefined) {
    //                                             // body += domElement.children[j].children[k].children[0].data + ". ";
    //                                             fs.appendFile("body.txt", domElement.children[j].children[k].children[0].data + ". ", (err) => {
    //                                                 if(err){
    //                                                     console.log(err);
    //                                                 }
    //                                             }); 
    //                                         }
    //                                     }
    //                                 }
    //                             }
                                
    //                         }
    //                     }
    //                 } else {
    //                     console.log("Det er en blog!");
    //                 }
    //                 return body;
    //             })
    //             .then(function(data) {
                       
    //             })
    //             .catch(function(err) {
    //                 console.log(err);
    //             });
    //         }
    //     }
    // })
    // .catch(function(err) {
    //     console.log("NOT OK");
    //     console.log(err);
    // });
    // body = "";
    // current_page++;
    // console.log(news_url + "?page=" + current_page);
// }

