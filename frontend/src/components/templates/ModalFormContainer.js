import Modal from 'react-modal';
import React, { useState } from 'react';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';

// With this template, its better to replace props.children with the specific component. That way, you avoid the difficulties of passing the close Modal logic up to the parent component. 

Modal.setAppElement('#app')

const ModalFormContainer = (props) => {
    const [modalisOpen, setModalisOpen] = useState(false);
    const handleClose = ()=>{setModalisOpen(false)}
    return(
        <>
            {(props.trigger ==="button") ?
                (<> <IconButton color="primary" aria-label={props.aria} onClick={() => setModalisOpen(true)}>{props.icon}<Typography variant="h6">{props.text}</Typography></IconButton></>):
                (<> <IconButton color="primary" aria-label={props.aria} onClick={() => setModalisOpen(true)}>{props.icon}</IconButton></>)}

            <Modal isOpen={modalisOpen} onClose={() => setModalisOpen(false)} onRequestClose={() => setModalisOpen(false)}>
                {props.children}
            </Modal>
            
        </>
    )
}

export default ModalFormContainer;