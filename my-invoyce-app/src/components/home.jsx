import { React, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../auth'
import Recipe from './Recipe'
import { Modal, Form, Button } from 'react-bootstrap'
import { useForm } from 'react-hook-form'

const LoggedinHome=()=>{
    const [ recipes, setRecipes ] = useState([]);
    const [ show, setShow ] = useState(false);
    const { register, reset, setValue, handleSubmit, formState:{errors} } = useForm()
    const [recipeId, setRecipeId]=useState(0);

    useEffect(
        ()=>{
            fetch('/api/recipe/recipes')
            .then(res=>res.json())
            .then(data=>{
                setRecipes(data)
            }
        )
            .catch(err=>console.log(err))
        },[]
    );

    const  getAllRecipes=()=>{
        fetch('/api/recipe/recipes')
                .then(res=>res.json())
                .then(data=>{
                    setRecipes(data)
                }
            )
                .catch(err=>console.log(err))
    }

    const closeModal=()=>{
        setShow(false)
    }

    const showModal=(id)=>{
        
        setShow(true)
        setRecipeId(id)

        recipes.map(
            (recipe)=>{
                if(recipe.id==id){
                    setValue('title',recipe.title)
                    setValue('description', recipe.description)
                }
            }
        )
    }
    let token=localStorage.getItem('REACT_TOKEN_AUTH_KEY')
    const updateRecipe=(data)=>{
        console.log(data)

        
        const requestOptions={
            method:'PUT',
            headers:{
                'content-type': 'application/json',
                'Authorization': `Bearer ${JSON.parse(token)}`
            },
            body:JSON.stringify(data)
        }

        fetch(`/api/recipe/recipe/${recipeId}`, requestOptions)
        .then(res=>res.json())
        .then(data=>{console.log(data)
            const reload = window.location.reload()
            reload()
        })
            
        .catch(err=>console.log(err))
    }

    const deleteRecipe=(id)=>{
        console.log(id)

        const requestOptions={
            method:'DELETE',
            headers:{
                'content-type': 'application/json',
                'Authorization': `Bearer ${JSON.parse(token)}`
            }
        }

        fetch(`/api/recipe/recipe/${id}`, requestOptions)
        .then(res=>res.json())
        .then(data=>{
            console.log(data)
            getAllRecipes()
        })
            
        .catch(err=>console.log(err))


    }


    return(
        <div className="recipes">
            <Modal 
                show={show} size="lg" onHide={() => setShow(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>
                        Update Recipe
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <form>
                        <Form.Group>
                            <Form.Label>Title</Form.Label>
                            <Form.Control type='text'
                                {...register('title', {required:true, maxLength: 30})}
                            />
                        </Form.Group>

                        {errors.title && <p style={{color:"red"}}><small>Title is Required</small></p>}
                        {errors.title?.type === "maxLength" && <p style={{color:"red"}}><small>Max Length is 30 characters</small></p>}

                        <Form.Group>
                            <Form.Label>Description</Form.Label>
                            <Form.Control as='textarea' rows={5}
                                {...register('description', {required:true, maxLength: 255})}
                            />
                        </Form.Group>

                        {errors.description && <p style={{color:"red"}}><small>Title is Required</small></p>}
                        {errors.description?.type === "maxLength" && <p style={{color:"red"}}><small>Max Length is 255 characters</small></p>}
                    
                        <Form.Group>
                            <Button variant='primary' onClick={handleSubmit(updateRecipe)}>
                                Save
                            </Button>
                        </Form.Group>
                    </form>
                </Modal.Body>
            </Modal>
            <h1>List of Recipes</h1>
            {
                recipes.map(
                    (recipe,index)=>(
                        <Recipe
                            title={recipe.title}
                            key={index}
                            description={recipe.description}
                            onClick={()=>{showModal(recipe.id)}}
                            onDelete={()=>{deleteRecipe(recipe.id)}}>

                        </Recipe>
                    )
                )
            }
        </div>
    )
}

const LoggedOutHome=()=>{
    return (
        <div>
            <h1 className="heading">Welcome to the Recipes</h1>
            <Link to='/signup' className="btn btn-primary btn-lg">Get Started</Link>
            <br></br>
            <br></br>
            Already have an account:
            <br></br>
            <Link to='/Login' className="btn btn-primary btn-lg">Login</Link>
        </div>
    )
}

const HomePage=()=>{
    const [ logged ]= useAuth()
    
    return(
        <div>
            {logged?<LoggedinHome/>:<LoggedOutHome/>}
        </div>
    )
}

export default HomePage