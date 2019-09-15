import React from 'react';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';

class Customer extends React.Component {
    render() {
        return (
            <TableRow>
                <TableCell><a href={this.props.data.split(",")[4].slice(2,-2)}>{this.props.number}</a></TableCell>
                <TableCell>{this.props.data}</TableCell>
            </TableRow>
        )
    }
}
export default Customer;
