import React, { useState } from 'react'
import { Form, Button } from 'react-bootstrap'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { login } from '../auth'



const LoginPage=()=>{
    const {register, handleSubmit, reset, formState:{errors} } = useForm()

    const navigate = useNavigate()

    const loginUser=(data)=>{
        console.log(data)

        const requestOptions={
            method:"POST",
            headers:{
                'content-type':'application/json'
            },
            body:JSON.stringify(data)

        }

        fetch('/api/auth/login', requestOptions)
        .then(res=>res.json())
        .then(data=>{
            console.log(data.access_token)
            login(data.access_token)

            navigate('/')
        })

        reset()
    }

    return(
        <div className="container1" >
        <div>
            <h1>Login Page</h1>
            <form>
                <Form.Group>
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="text" className="form"
                        placeholder="Your Username"
                        {...register('username', {required:true, maxLength:25})}
                    />
                <br></br>
                </Form.Group>
                
                {errors.username && <p style={{color:"red"}}><small>Username is required</small></p>}
                {errors.username?.type === "maxLength" && <p style={{color:"red"}}><small>Max Length is 25 characters</small></p>}
                
                <Form.Group>
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password"  
                        className="form"
                        placeholder="Your Password"
                        {...register('password', {required:true, minLength:8})}
                    />
                <br></br>
                </Form.Group>

                {errors.password && <p style={{color:"red"}}><small>Password is required</small></p>}
                {errors.password?.type === "minLength" && <p style={{color:"red"}}><small>Min Password length is 8 characters</small></p>}
                
                <Form.Group>
                    <Button as="sub" variant="primary" onClick={handleSubmit(loginUser)}>Log In</Button>
                </Form.Group>
                <br></br>
                <Form.Group>
                    <small>Do not have an account <Link to='/signUp'>Create one</Link> </small>
                </Form.Group>
            </form>
        </div>
    </div>

    )
}

export default LoginPage