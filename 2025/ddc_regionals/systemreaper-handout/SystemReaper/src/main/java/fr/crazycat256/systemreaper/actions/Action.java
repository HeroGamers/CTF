package fr.crazycat256.systemreaper.actions;

public abstract class Action {

    public final String ip;

    public Action(String ip) {
        this.ip = ip;
    }

    public abstract String getDescription();
    public abstract void execute();


}
