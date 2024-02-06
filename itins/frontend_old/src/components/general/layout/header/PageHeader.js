import React from 'react'
import { Paper, Card, Typography, makeStyles, Button } from '@material-ui/core'

const useStyles = makeStyles(theme => ({
    root: {
        backgroundColor: '#fdfdgh'
    },
    pageHeader:{
        padding:theme.spacing(4),
        display:'flex',
        marginBottom:theme.spacing(2),
        marginTop:theme.spacing(5)

    },
    pageIcon:{
        display:'inline-block',
        padding:theme.spacing(1),
        marginLeft:theme.spacing(35),

        color:'#3c44b1'
    },
    pageTitle:{
        paddingLeft:theme.spacing(4),
        '& .MuiTypography-subtitle1':{
            opacity:'0.8'
        }
    }
}))

export default function PageHeader(props) {

    const styles = useStyles();
    const { header, subHeader, icon } = props;
    return (
        <Paper elevation={0} square className={styles.root}>
            <div className={styles.pageHeader}>
                <Card className={styles.pageIcon}>
                    {icon}
                </Card>
                <div className={styles.pageTitle}>
                    <Typography
                        variant="h5"
                        component="div">
                        {header}</Typography>
                    <Typography
                        variant="subtitle1"
                        component="div">
                        {subHeader}</Typography>
                </div>
            </div>
        </Paper>
    )
}