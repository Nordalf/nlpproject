const request = require('request');
const async = require('async');
const fs = require('fs');
const $ = require('cheerio');
const base_url = 'https://www.dr.dk';
const news_url = 'https://www.dr.dk/nyheder/allenyheder';

var drURLS = [];

var notCurrentDate = true;

var next_page_url = 'https://www.dr.dk/nyheder/allenyheder';

var date_representation = '';

var dates = [];

for(let i = 2008; i < 2010; i++) {
    for(let j = 1; j < 13; j++) {
        for(let k = 1; k < 29; k++) {
            if(k < 10) { // Dag under 10
                if(j < 10) { // Maaned under 10
                    date_representation = "0" + k + "0" + j + "" + i;
                    dates.push(date_representation)
                } else {
                    date_representation = "0" + k + "" + j + "" + i;
                    dates.push(date_representation)
                }
            } else {
                if(j < 10) { // Maaned under 10
                    date_representation = "" + k + "0" + j + "" + i;
                    dates.push(date_representation)
                } else {
                    date_representation = "" + k + "" + j + "" + i;
                    dates.push(date_representation)
                }
            }
        }
    }    
}

var date_index = 0;

async.whilst(
    function conditionChecker(callbackFunction) {
        callbackFunction(null, notCurrentDate);
    }, 
    function makeRequestAndGetArticles(next) {
        request(next_page_url + "/" + dates[date_index], (err, res, html) => {
            console.log(dates[date_index]);
            if(err) { 
                return console.log(err); 
            }

        
            for(let i = 0; i < $('.dr-list:nth-child(1) > article > h3', html).length; i++) {
                drURLS.push($('.dr-list:nth-child(1) > article > h3', html)[i].children[0].attribs.href);
            }

            for(let i = 0; i < drURLS.length; i++) {
                
                request(base_url + drURLS[i], (err, res, html) => {
                    if(err) { 
                        return console.log(err); 
                    }
                    
                    var article_paragraph_length = $('.dre-container__content > .dre-speech', html).length;
                    for(let i = 0; i < article_paragraph_length; i++) {
                        if($('.dre-container__content > .dre-speech > p', html)[i] != undefined) { // Sandsynligvis en header
                            fs.appendFileSync("drdkcorpus.txt", $('.dre-container__content > .dre-speech > p', html)[i].children[0].data + "\n");
                        }
                    }
                });
            }

            drURLS = [];
            if (date_index == 10) {
                notCurrentDate = true;    
            }
            date_index++;
            setTimeout(() => {
                next(null,next_page_url);
            }, 1000);
        });
    }, 
    function(err, n) {
        console.log("Everything went fine: " + n );
        if(err) return;
    });
