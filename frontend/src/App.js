import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import TableRow from '@material-ui/core/TableRow'
import TableCell from '@material-ui/core/TableCell'
import Table from '@material-ui/core/Table';
import TableHead from '@material-ui/core/TableHead';
import TableBody from '@material-ui/core/TableBody';

import Customer from './Customer'

const styles = theme => ({
    root: {
    width: "100%",
    marginTop: theme.spacing.unit * 3,
    overflowX: "auto"
    },
    table: {
    minWidth: 1080
    }
});

class App extends Component {
    state = {
        posts: []
    };

    async componentDidMount() {
        try {
            const res = await fetch('http://127.0.0.1:8000/api/crawl/');
            const posts = await res.json();
            this.setState({
                posts
            });
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        return (
            <div>
                <div>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>번호</TableCell>
                                <TableCell>데이터</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {this.state.posts.map(item => (<Customer key={item.id} number={item.number} data={item.data}/>))}
                        </TableBody>
                    </Table>
                </div>
            </div>
        );
    }
}

export default App;
