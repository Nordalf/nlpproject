import React from 'react';
import logo from './logo.svg';
import './App.css';
import TextareaAutosize from '@material-ui/core/TextareaAutosize';
 
class NERForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: 'Write in text to be anonymized',
      result: 'Result is put here'
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
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
      
      if(!response.status == 200) 
      {
          alert("Response status code is not 200");
      }
      return response.json()
    }).then(data => {
      this.setState({result: data.data});
    });
    
    event.preventDefault();
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <form onSubmit={this.handleSubmit}>
            <label>
              Text to be anonymized:
              <br />
              <TextareaAutosize value={this.state.value} onChange={this.handleChange} />
            </label>
            <input type="submit" value="Submit" />
          </form>
          <br />
          <TextareaAutosize value={this.state.result}/>
        </header>
        
      </div>
    );
  }
}
export default NERForm;
