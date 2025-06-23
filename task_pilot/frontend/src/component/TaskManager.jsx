import React from 'react'
import { useEffect } from 'react'
import { useState } from 'react'
import axios from 'axios';

const API = 'http://localhost:5000';
const TaskManager = () => {
  const [tasks,setTasks]=useState([])
  const [form,setForm]=useState({title:'',description:''})
useEffect(()=>{
  fetchTask();
},[])
const fetchTask=async()=>{
  const res=await axios.get(`${API}/fetch-mytasks`);
  setTasks(res.data);

};
const addTask=async()=>{
  e.preventDefault()
  const res=await axios.post(`${API}/add-todo`,form);
  setForm({title:'',description:''});
  fetchTask();
}
const deleteTask=async()=>{
  await axios.delete(`${API}/remove-task/${id}`)
  fetchTask();
}
  return (
    <div>
     <form onSubmit={addTask}>
        <input
          type="text"
          placeholder="Title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Description"
          value={form.description}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          required
        />
        <button type="submit">Add Task</button>
      </form>
<ul>
  {
    tasks.map((task)=>(
      <li key={task._id}>
        <strong>{task.title}</strong>-{task.description}
        <br/>
        Status: {task.completed ? '✅ Done' : '❌ Pending'}
        <br/>
        {!task.completed && <button onClick={() => markDone(task._id)}>Mark Done</button>}
            <button onClick={() => deleteTask(task._id)} style={{ marginLeft: 10 }}>Delete</button>
      </li>
    
  ))}
</ul>
    </div>
  )
}

export default TaskManager
