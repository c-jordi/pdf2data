import {TickInput} from "../../inputs"


const renderMetrics = (metrics) => {
    const table = {
        header : [],
        body : []
    }
    metrics._fields.forEach(field => {
        table.header.push(field)
        table.body.push(metrics[field])
    })

    return <table className="metrics">
        <tbody>
        <tr>{table.body.map(el => <td key={'b-'+el}>{el}</td>)}</tr>
        </tbody>
        <tfoot>
        <tr>{table.header.map(el => <th key={'h-'+el}>{el.replace(/^\w/, (c) => c.toUpperCase())}</th>)}</tr>
        </tfoot>
    </table>
}

const ItemChild = ({data}) => {
    return <div className="item-child">
        <TickInput/>
        <div className="label">{data.label}</div>
        {renderMetrics(data.metrics)}
    </div>
}

export default ItemChild;