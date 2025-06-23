const express=require('express')
const  mongoose=reuire('mongoose')
const cors=require('cors')
require('dotenv').config();

const Task=reuire('./models/Task');
const app=express();
app.use(cors())
app.use(express.json())

const mongo_url=process.env.MONGO_URL||'mongodb://localhost:27017/taskpilot';

mongoose.connect(mongo_url).then(()=>console.log("cpnnectd"))
                            .catch(()=>console.error(err));
                            

app.get('/get-tasks',async(req,res)=>{
  const tasks=await Task.find();
  res.json(tasks)
})                            
app.post('add-task',async(req,res)=>{
  const task=new Task(req.body);
  await task.save();
  res.json(task)
})
app.put('/mark-done/:id', async (req, res) => {
  const task = await Task.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(task);
});
app.delete('/remove-task/:id', async (req, res) => {
  await Task.findByIdAndDelete(req.params.id);
  res.json({ message: "Task deleted" });
});
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});