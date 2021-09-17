import {SearchInput,TickInput} from  "../"
import "./style.scss"

const FilterInput = () => {
    return <div className="d-filter-input">
        <div className='label'>
            Filter
        </div>
        <SearchInput style={{marginTop: "12px"}}></SearchInput>
        <div className="flex-row" style={{marginTop: "12px"}}>
        <TickInput label={"Labels"}></TickInput>
        <TickInput label={"Flags"}></TickInput>
        </div>
    </div>
}

export default FilterInput;