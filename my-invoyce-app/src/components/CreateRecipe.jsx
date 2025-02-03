import React from 'react'
import { Form, Button } from 'react-bootstrap'
import { useForm } from 'react-hook-form'

const CreateRecipePage=()=>{

    const { register, handleSubmit, reset, formState:{errors} } = useForm()

    const createRecipe=(data)=>{
        console.log(data)
        const token=localStorage.getItem('REACT_TOKEN_AUTH_KEY')
        console.log(token)

        const requestOptions={
            method:'POST',
            headers:{
                'content-type': 'application/json',
                'Authorization': `Bearer ${JSON.parse(token)}`
            },
            body:JSON.stringify(data)
        }
        fetch('/api/recipe/recipes', requestOptions)
        .then(res=>res.json())
        .then(data=>{
            reset()
        })
        .catch(err=>console.log(err))
    }

    return(
        <div className="container1" >
            <h1>Create a Recipe</h1>
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
                    <Button variant='primary' onClick={handleSubmit(createRecipe)}>
                        Save
                    </Button>
                </Form.Group>
            </form>
        </div>

    )
}

export default CreateRecipePage