import React from 'react';
import './App.css';
import Button from '@material-ui/core/Button';
import TextareaAutosize from '@material-ui/core/TextareaAutosize';
 
// var previous_sentence = '';
// var next_sentence_start_position = 0;
// var sequence_to_send = '';

class NERForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: '',
      result: '',
      previous_was_punctuation: false,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleKeyDown = (event) => 
  {
    // if (event.which === 46) 
    // {
    //   previous_sentence = '';
    //   next_sentence_start_position = 0;
    //   sequence_to_send = '';      
    // } 
    // else 
    // {
    //   sequence_to_send = event.target.value;
    //   if (this.state.previous_was_punctuation && event.which === 32) 
    //   {
    //     if(next_sentence_start_position === 0) 
    //     {
    //       previous_sentence = sequence_to_send.slice(0, sequence_to_send.indexOf(".") + 1); // +1 for taking care of whitespace
    //       next_sentence_start_position = previous_sentence.length;
    //       console.log("PREV: " + previous_sentence)
    //     } 
    //     else 
    //     {
    //       next_sentence_start_position = sequence_to_send.length - next_sentence_start_position;
    //       previous_sentence = sequence_to_send.slice(next_sentence_start_position);
    //     }
    //     console.log(previous_sentence);
    //   }
    // }

    if (this.state.previous_was_punctuation && event.which === 32) {
      this.handleSubmit(event);
    }
    if (event.which === 190 || event.which === 187) {
      this.state.previous_was_punctuation = true;
    } else {
      this.state.previous_was_punctuation = false;
    }
    
  }

  handleSubmit(event) {
    const obj = {
      data: this.state.value
    };
    // alert('Text to be processed has been submitted: ' + this.state.value);
    fetch("http://localhost:5000/api/v1/anonymize/text", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(obj.data)
    })
    .then(response => {
      
      if(!response.status === 200) 
      {
          alert("Response status code is not 200");
      }
      return response.json()
    }).then(data => {
      let result = "";
      data.data.forEach(element => {
        if(element.tag !== 'O'){
          result += element.word + " {" + element.tag + "} ";
        }
        else {
          result += element.word + " ";
        }
      });
      this.setState({result: result});
    });
    
    event.preventDefault();
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <form onSubmit={this.handleSubmit} className="Anon-form">
            <label>
              Text to be anonymized:
              <br />
              <TextareaAutosize rowsMin={10} value={this.state.value} onChange={this.handleChange} style = {{width: '100%', fontSize:20}} onKeyUp={this.handleKeyDown} placeholder='Write in text to be anonymized'/>
            </label>
            <br />
            <Button type="submit" variant="contained" size="large" color="primary">
            Submit
            </Button>
          </form>
          <br />
          <div className="Anon-form">
            <TextareaAutosize rowsMin={10} value={this.state.result} style = {{width: '100%', fontSize:20}} placeholder='Results are shown here!'/>
          </div>
        </header>
        
      </div>
    );
  }
}
export default NERForm;
