import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import moment from 'moment';
import { useHistory } from "react-router-dom"; 

function Todos({isAuthenticated, setIsAuthenticated}) {
	const [todos, setTodos] = useState([]);
	const [changed, setChanged] = useState(false);
	const [errorMessage, setErrorMessage] = useState('');
	const [page, setPageNumber] = useState(1);
	const [n, setPageSize] = useState(5);
	const [inputPageNumber, setInputPageNumber] = useState(page);
	const [inputPageSize, setInputPageSize] = useState(n);
	const [filter, setFilter] = useState("All");
	let history = useHistory();

	useEffect(() => {
		if(!isAuthenticated){
			history.push("/");
		}
	}, [isAuthenticated, history])

	useEffect(() => {
		const loadData = async () => {
			let response = null;
			try {
                const backend_url = process.env.REACT_APP_BACKEND_URL;

				let url = `${backend_url}/task_manager/task/?page=${page}&n=${n}`;

				if(filter === 'Completed'){
					url = `${backend_url}/task_manager/task/?page=${page}&n=${n}&is_completed=true`;
				} else if(filter === 'Not Completed'){
					url = `${backend_url}/task_manager/task/?page=${page}&n=${n}&is_completed=false`;
				}
				
				response = await axios.get(url, {withCredentials: true,});
			} catch(error){
				if (error.response) {
					setErrorMessage(error.response.data.message);
				} else {
					setErrorMessage('Error: something happened');
				}
				return;
			}
			setErrorMessage('');
			setTodos(response.data);
		}

		loadData();
	}, [changed, page, n, filter])

	const nextPage = () => {
		setPageNumber(page + 1);
		setInputPageNumber(page + 1);
	}

	const previousPage = () => {
		if(page > 1){
			setPageNumber(page - 1);
			setInputPageNumber(page - 1);
		}
	}

	const enterPageNumber = (enteredPageNumber) => {
		if(enteredPageNumber >= 1){
			setPageNumber(parseInt(enteredPageNumber));
		} else {
			setPageNumber(1);
			setInputPageNumber(1);
		}
	}

	const enterPageSize = (enteredPageSize) => {
		if(enteredPageSize >= 1){
			setPageSize(parseInt(enteredPageSize));
		} else {
			setPageSize(1);
			setInputPageSize(1);
		}
	}

	const pageNumberControl = () => {
		return <div>
			<center>
				<div className="input-group col-lg-4 col-md-6 col-sm-8 col-9">
					<div className="input-group-append">
						<button className="btn btn-outline-secondary" onClick={() => previousPage()} >Previous Page</button>
					</div>
					<input className="form-control text-center" type="number" value={inputPageNumber} onChange={e => setInputPageNumber(e.target.value)} onKeyPress={e => {
									if (e.key === 'Enter') {
										enterPageNumber(e.target.value)
									}
								}}/>
					<div className="input-group-append">
						<button className="btn btn-outline-secondary" onClick={() => nextPage()}>Next Page</button>
					</div>
				</div>
			</center>
		</div>
	}

	const pageSizeControl = () => {
		return <center>
			<div className="input-group col-xl-3 col-md-4 col-sm-5 col-6">
				<div className="input-group-append">
					<span className="input-group-text" id="">Todo per page: </span>
				</div>
				<input className="form-control text-center" type="number" value={inputPageSize} onChange={e => setInputPageSize(e.target.value)} onKeyPress={e => {
								if (e.key === 'Enter') {
									enterPageSize(e.target.value)
								}
							}}
				/>
			</div>
		</center>
	}

	const filterControl = () => {
		return <center>
			<div className="col-6 offset-8">
				<label>Show</label>
				<select value={filter} onChange={(e) => setFilter(e.target.value)}>
					<option value="All">All</option>
					<option value="Completed">Completed</option>
					<option value="Not Completed">NotCompleted</option>
				</select>
			</div>
		</center>
	}

	const markCompleted = async (id) => {
		try {
      const backend_url = process.env.REACT_APP_BACKEND_URL;

      await axios.patch(`${backend_url}/task_manager/task/update`,
             {'is_completed': true, 'task_id': id} , {
				withCredentials: true
			});
    } catch(error){
      if (error.response) {
        setErrorMessage(error.response.data.message);
      } else {
        setErrorMessage('Error: something happened');
      }
      return;
		}
		setErrorMessage('');
		setChanged(!changed);
	}

	const deleteTodo = async (id) => {
        try {
            console.log('ID',id)
            const backend_url = process.env.REACT_APP_BACKEND_URL;

            await axios.delete(`${backend_url}/task_manager/task/delete/${id}`,
             {
                withCredentials: true,
            });
        } catch(error){
          if (error.response) {
            setErrorMessage(error.response.data.message);
          } else {
            setErrorMessage('Error: something happened');
          }
          return;
            }
            setErrorMessage('');
            setChanged(!changed);
        }

	const showErrorMessage = () => {
    if(errorMessage === ''){
      return <div></div>
    }

    return <div className="alert alert-danger" role="alert">
      {errorMessage}
    </div>
  }

	return (
		<div className="container">
			<h1 className="text-center">Todo List</h1>
			{showErrorMessage()}
			
			{filterControl()}
			
      <table className="table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Target Date</th>
            <th>Is Completed?</th>
						<th>Mark Completed</th>
						<th>Update</th>
						<th>Delete</th>
          </tr>
        </thead>
        <tbody>
        {
          todos.map((todo) => {
            return <tr className={todo.is_completed? 'completed' : ''} key={todo.id}>
              <td>{todo.title}</td>
              <td>{moment(todo.target_date).format('ll')}</td>
              <td>{todo.is_completed.toString()}</td>
							<td><button className="btn btn-success" onClick={() => markCompleted(todo.id)}>Mark Completed</button></td>
							<td><Link to={{pathname: `/update/${todo.id}`}}><button className="btn btn-primary">Update</button></Link></td>
							<td><button className="btn btn-danger" onClick={() => deleteTodo(todo.id)}>Delete</button></td>
            </tr>
          })
        }
        </tbody>
      </table>
			{pageSizeControl()}
			{pageNumberControl()}
    </div>
	);
}

export default Todos;