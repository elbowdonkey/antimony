#ifndef EVAL_H
#define EVAL_H

#include <Python.h>
#include "datum/datum.h"


class EvalDatum : public Datum
{
    Q_OBJECT
public:
    explicit EvalDatum(QString name, QObject* parent=0);

    QString getExpr() const { return expr; }
    void setExpr(QString new_expr);
protected:
    virtual PyObject* getCurrentValue() const;
    virtual bool validate(PyObject* v) const;

    QString expr;
};

#endif // EVAL_H
