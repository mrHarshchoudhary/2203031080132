const express=require('express');
const router=express.Router();
let books=[];
let id=1;
//get all books
router.get('/',(req,res)=>{
  res.json(books);
})

//post
router.post('/',(req,res)=>{
  const{title,author,price}=req.body;
  if (!title || !author || !price) {
    return res.status(400).json({ message: 'All fields required' });
  }
  const newBook={id:id++,title,author,price}
  books.push(newBook);
  res.status(201).json(newBook);
})
router.delete('/:id',(req,res)=> {
  const bookId=parseInt(req.params.id)
   books = books.filter(book => book.id !== bookId);
  res.json({ message: 'Book deleted successfully' });
})
module.exports=router